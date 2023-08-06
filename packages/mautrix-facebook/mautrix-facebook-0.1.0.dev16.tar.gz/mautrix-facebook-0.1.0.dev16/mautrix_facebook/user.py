# mautrix-facebook - A Matrix-Facebook Messenger puppeting bridge
# Copyright (C) 2019 Tulir Asokan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Any, Dict, Iterator, Optional, Iterable, Awaitable, TYPE_CHECKING
from http.cookies import SimpleCookie
import asyncio
import logging

from fbchat import Client, Message, ThreadType, User as FBUser, ActiveStatus, MessageReaction

from mautrix.types import UserID, PresenceState
from mautrix.appservice import AppService
from mautrix.client import Client as MxClient
from mautrix.bridge._community import CommunityHelper, CommunityID

from .config import Config
from .commands import enter_2fa_code
from .db import User as DBUser, UserPortal as DBUserPortal, Contact as DBContact
from . import portal as po, puppet as pu

if TYPE_CHECKING:
    from .context import Context

config: Config


class User(Client):
    az: AppService
    loop: asyncio.AbstractEventLoop
    log: logging.Logger = logging.getLogger("mau.user")
    by_mxid: Dict[UserID, 'User'] = {}
    by_fbid: Dict[str, 'User'] = {}

    user_agent: str

    command_status: Optional[Dict[str, Any]]
    is_whitelisted: bool
    is_admin: bool
    permission_level: str
    _is_logged_in: Optional[bool]
    _session_data: Optional[SimpleCookie]
    _db_instance: Optional[DBUser]

    _community_helper: CommunityHelper
    _community_id: Optional[CommunityID]

    def __init__(self, mxid: UserID, session: Optional[SimpleCookie] = None,
                 user_agent: Optional[str] = None, db_instance: Optional[DBUser] = None) -> None:
        super().__init__(loop=self.loop)
        self.mxid = mxid
        self.by_mxid[mxid] = self
        self.user_agent = user_agent
        self.command_status = None
        self.is_whitelisted, self.is_admin, self.permission_level = config.get_permissions(mxid)
        self._is_logged_in = None
        self._session_data = session
        self._db_instance = db_instance
        self._community_id = None

        self.log = self.log.getChild(self.mxid)
        self._log = self._log.getChild(self.mxid)
        self._req_log = self._req_log.getChild(self.mxid)
        self._util_log = self._util_log.getChild(self.mxid)
        self.set_active_status(False)

    # region Sessions

    @property
    def fbid(self) -> str:
        return self.uid

    @property
    def db_instance(self) -> DBUser:
        if not self._db_instance:
            self._db_instance = DBUser(mxid=self.mxid, session=self._session_data, fbid=self.uid,
                                       user_agent=self.user_agent)
        return self._db_instance

    def save(self, _update_session_data: bool = True) -> None:
        self.log.debug("Saving session")
        if _update_session_data:
            self._session_data = self.get_session()
        self.db_instance.edit(session=self._session_data, fbid=self.uid,
                              user_agent=self.user_agent)

    @classmethod
    def from_db(cls, db_user: DBUser) -> 'User':
        return User(mxid=db_user.mxid, session=db_user.session, user_agent=db_user.user_agent,
                    db_instance=db_user)

    @classmethod
    def get_all(cls) -> Iterator['User']:
        for db_user in DBUser.all():
            yield cls.from_db(db_user)

    @classmethod
    def get_by_mxid(cls, mxid: UserID, create: bool = True) -> Optional['User']:
        if pu.Puppet.get_id_from_mxid(mxid) is not None or mxid == cls.az.bot_mxid:
            return None
        try:
            return cls.by_mxid[mxid]
        except KeyError:
            pass

        db_user = DBUser.get_by_mxid(mxid)
        if db_user:
            return cls.from_db(db_user)

        if create:
            user = cls(mxid)
            user.db_instance.insert()
            return user

        return None

    @classmethod
    def get_by_fbid(cls, fbid: str) -> Optional['User']:
        try:
            return cls.by_fbid[fbid]
        except KeyError:
            pass

        db_user = DBUser.get_by_fbid(fbid)
        if db_user:
            return cls.from_db(db_user)

        return None

    async def load_session(self) -> bool:
        if self._is_logged_in:
            return True
        elif not self._session_data:
            return False
        ok = (await self.set_session(self._session_data, user_agent=self.user_agent)
              and await self.is_logged_in(True))
        if ok:
            self.log.info("Loaded session successfully")
            self.listen(long_polling=False, mqtt=True)
            asyncio.ensure_future(self.post_login(), loop=self.loop)
        return ok

    async def is_logged_in(self, _override: bool = False) -> bool:
        if self._is_logged_in is None or _override:
            self._is_logged_in = await super().is_logged_in()
        return self._is_logged_in

    # endregion

    async def logout(self, safe: bool = False) -> bool:
        self.stop_listening()
        ok = await super().logout(safe)
        self._session_data = None
        self._is_logged_in = False
        self.save(_update_session_data=False)
        return ok

    async def post_login(self) -> None:
        self.log.info("Running post-login actions")
        self.by_fbid[self.fbid] = self

        try:
            puppet = pu.Puppet.get_by_fbid(self.fbid)

            if puppet.custom_mxid != self.mxid and puppet.can_auto_login(self.mxid):
                self.log.info(f"Automatically enabling custom puppet")
                await puppet.switch_mxid(access_token="auto", mxid=self.mxid)
        except Exception:
            self.log.exception("Failed to automatically enable custom puppet")

        await self._create_community()
        await self.sync_contacts()
        await self.sync_threads()
        self.log.debug("Updating own puppet info")
        own_info = (await self.fetch_user_info(self.uid))[self.uid]
        puppet = pu.Puppet.get_by_fbid(self.uid, create=True)
        await puppet.update_info(source=self, info=own_info)

    async def _create_community(self) -> None:
        template = config["bridge.community_template"]
        if not template:
            return
        localpart, server = MxClient.parse_user_id(self.mxid)
        community_localpart = template.format(localpart=localpart, server=server)
        self.log.debug(f"Creating personal filtering community {community_localpart}...")
        self._community_id, created = await self._community_helper.create(community_localpart)
        if created:
            await self._community_helper.update(self._community_id, name="Facebook Messenger",
                                                avatar_url=config["appservice.bot_avatar"],
                                                short_desc="Your Facebook bridged chats")
            await self._community_helper.invite(self._community_id, self.mxid)

    async def _add_community(self, up: Optional[DBUserPortal], contact: Optional[DBContact],
                             portal: 'po.Portal', puppet: Optional['pu.Puppet']) -> None:
        if portal.mxid:
            if not up or not up.in_community:
                ic = await self._community_helper.add_room(self._community_id, portal.mxid)
                if up and ic:
                    up.edit(in_community=True)
                elif not up:
                    DBUserPortal(user=self.fbid, in_community=ic, portal=portal.fbid,
                                 portal_receiver=portal.fb_receiver).insert()
        if puppet:
            await self._add_community_puppet(contact, puppet)

    async def _add_community_puppet(self, contact: Optional[DBContact],
                                    puppet: 'pu.Puppet') -> None:
        if not contact or not contact.in_community:
            await puppet.default_mxid_intent.ensure_registered()
            ic = await self._community_helper.join(self._community_id,
                                                   puppet.default_mxid_intent)
            if contact and ic:
                contact.edit(in_community=True)
            elif not contact:
                DBContact(user=self.fbid, contact=puppet.fbid, in_community=ic).insert()

    async def sync_contacts(self):
        try:
            self.log.debug("Fetching contacts...")
            users = await self.fetch_all_users()
            self.log.debug(f"Fetched {len(users)} contacts")
            contacts = DBContact.all(self.fbid)
            update_avatars = config["bridge.update_avatar_initial_sync"]
            for user in users:
                puppet = pu.Puppet.get_by_fbid(user.uid, create=True)
                await puppet.update_info(self, user, update_avatar=update_avatars)
                await self._add_community_puppet(contacts.get(puppet.fbid, None), puppet)
        except Exception:
            self.log.exception("Failed to sync contacts")

    async def sync_threads(self) -> None:
        try:
            sync_count = min(20, config["bridge.initial_chat_sync"])
            if sync_count <= 0:
                return
            self.log.debug("Fetching threads...")
            threads = await self.fetch_thread_list(limit=sync_count)
            ups = DBUserPortal.all(self.fbid)
            contacts = DBContact.all(self.fbid)
            for thread in threads:
                self.log.debug(f"Syncing thread {thread.uid} {thread.name}")
                fb_receiver = self.uid if thread.type == ThreadType.USER else None
                portal = po.Portal.get_by_thread(thread, fb_receiver)
                puppet = None

                if isinstance(thread, FBUser):
                    puppet = pu.Puppet.get_by_fbid(thread.uid, create=True)
                    await puppet.update_info(self, thread)

                await self._add_community(ups.get(portal.fbid, None),
                                          contacts.get(puppet.fbid, None) if puppet else None,
                                          portal, puppet)

                await portal.create_matrix_room(self, thread)
        except Exception:
            self.log.exception("Failed to sync threads")

    # region Facebook event handling

    async def on_logging_in(self, email: str = None) -> None:
        self.log.info("Logging in {}...".format(email))

    async def on_2fa_code(self) -> str:
        if self.command_status and self.command_status.get("action", "") == "Login":
            future = self.loop.create_future()
            self.command_status["future"] = future
            self.command_status["next"] = enter_2fa_code
            await self.az.intent.send_notice(self.command_status["room_id"],
                                             "You have two-factor authentication enabled. "
                                             "Please send the code here.")
            return await future
        self.log.warning("Unexpected on2FACode call")
        # raise RuntimeError("No ongoing login command")

    async def on_logged_in(self, email: str = None) -> None:
        """
        Called when the client is successfully logged in

        :param email: The email of the client
        """
        self._is_logged_in = True
        if self.command_status and self.command_status.get("action", "") == "Login":
            await self.az.intent.send_notice(self.command_status["room_id"],
                                             f"Successfully logged in with {email}")
            self.save()
            self.listen(long_polling=False, mqtt=True)
            asyncio.ensure_future(self.post_login(), loop=self.loop)
        self.log.warning("Unexpected onLoggedIn call")
        # raise RuntimeError("No ongoing login command")

    async def on_listening(self) -> None:
        """Called when the client is listening."""
        self.log.info("Listening with long polling...")

    async def on_listening_mqtt(self) -> None:
        """Called when the client is listening with MQTT."""
        self.log.info("Listening with MQTT...")

    async def on_listen_error(self, exception: Exception = None) -> bool:
        """
        Called when an error was encountered while listening

        :param exception: The exception that was encountered
        :return: Whether the loop should keep running
        """
        self.log.exception("Got exception while listening, reconnecting in 10s")
        await asyncio.sleep(10)
        return True

    async def on_mqtt_fatal_error(self, exception: Exception = None) -> bool:
        """Called when an error was encountered while listening.

        Args:
            exception: The exception that was encountered

        Returns:
            Whether the client should reconnect
        """
        self.log.exception("MQTT connection failed, reconnecting in 10s")
        await asyncio.sleep(10)
        return True

    async def on_mqtt_parse_error(self, event_type=None, event_data=None, exception=None):
        """Called when an error was encountered while parsing a MQTT message.

        Args:
            event_type: The event type
            event_data: The event data, either as a bytearray if JSON decoding failed or as a dict
                if JSON decoding was successful.
            exception: The exception that was encountered
        """
        if isinstance(event_data, bytearray):
            self.log.warning(f"MQTT JSON decoder error: {exception}")
        else:
            self.log.exception("Failed to parse MQTT message: %s", event_data)

    async def on_message(self, mid: str = None, author_id: str = None, message: str = None,
                         message_object: Message = None, thread_id: str = None,
                         thread_type: ThreadType = ThreadType.USER, at: int = None,
                         metadata: Any = None, msg: Any = None) -> None:
        """
        Called when the client is listening, and somebody sends a message

        :param mid: The message ID
        :param author_id: The ID of the author
        :param message: (deprecated. Use `message_object.text` instead)
        :param message_object: The message (As a `Message` object)
        :param thread_id: Thread ID that the message was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the message was sent to. See :ref:`intro_threads`
        :param at: The timestamp of the message
        :param metadata: Extra metadata about the message
        :param msg: A full set of the data recieved
        :type message_object: models.Message
        :type thread_type: models.ThreadType
        """
        self.log.debug(f"onMessage({message_object}, {thread_id}, {thread_type})")
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver, thread_type)
        puppet = pu.Puppet.get_by_fbid(author_id)
        if not puppet.name:
            await puppet.update_info(self)
        message_object.uid = mid
        await portal.handle_facebook_message(self, puppet, message_object)

    async def on_color_change(self, mid=None, author_id=None, new_color=None, thread_id=None,
                              thread_type=ThreadType.USER, at=None, metadata=None, msg=None
                              ) -> None:
        """
        Called when the client is listening, and somebody changes a thread's color

        :param mid: The action ID
        :param author_id: The ID of the person who changed the color
        :param new_color: The new color
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type new_color: models.ThreadColor
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "Color change from {} in {} ({}): {}".format(
                author_id, thread_id, thread_type.name, new_color
            )
        )

    async def on_emoji_change(self, mid=None, author_id=None, new_emoji=None, thread_id=None,
                              thread_type=ThreadType.USER, at=None, metadata=None, msg=None
                              ) -> None:
        """
        Called when the client is listening, and somebody changes a thread's emoji

        :param mid: The action ID
        :param author_id: The ID of the person who changed the emoji
        :param new_emoji: The new emoji
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "Emoji change from {} in {} ({}): {}".format(
                author_id, thread_id, thread_type.name, new_emoji
            )
        )

    async def on_title_change(self, mid=None, author_id=None, new_title=None, thread_id=None,
                              thread_type=ThreadType.USER, at=None, metadata=None, msg=None
                              ) -> None:
        """
        Called when the client is listening, and somebody changes the title of a thread

        :param mid: The action ID
        :param author_id: The ID of the person who changed the title
        :param new_title: The new title
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver)
        if not portal:
            return
        sender = pu.Puppet.get_by_fbid(author_id)
        if not sender:
            return
        await portal.handle_facebook_name(self, sender, new_title, mid)

    async def on_image_change(self, mid: str = None, author_id: str = None, new_image: str = None,
                              thread_id: str = None, thread_type: ThreadType = ThreadType.GROUP,
                              at: int = None, msg: Any = None) -> None:
        """
        Called when the client is listening, and somebody changes the image of a thread

        :param mid: The action ID
        :param author_id: The ID of the person who changed the image
        :param new_image: The ID of the new image
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver)
        if not portal:
            return
        sender = pu.Puppet.get_by_fbid(author_id)
        if not sender:
            return
        await portal.handle_facebook_photo(self, sender, new_image, mid)

    async def on_nickname_change(self, mid=None, author_id=None, changed_for=None,
                                 new_nickname=None,
                                 thread_id=None, thread_type=ThreadType.USER, at=None,
                                 metadata=None,
                                 msg=None) -> None:
        """
        Called when the client is listening, and somebody changes the nickname of a person

        :param mid: The action ID
        :param author_id: The ID of the person who changed the nickname
        :param changed_for: The ID of the person whom got their nickname changed
        :param new_nickname: The new nickname
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "Nickname change from {} in {} ({}) for {}: {}".format(
                author_id, thread_id, thread_type.name, changed_for, new_nickname
            )
        )

    async def on_admin_added(self, mid=None, added_id=None, author_id=None, thread_id=None,
                             thread_type=ThreadType.GROUP, at=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody adds an admin to a group thread

        :param mid: The action ID
        :param added_id: The ID of the admin who got added
        :param author_id: The ID of the person who added the admins
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        self.log.info("{} added admin: {} in {}".format(author_id, added_id, thread_id))

    async def on_admin_removed(self, mid=None, removed_id=None, author_id=None, thread_id=None,
                               thread_type=ThreadType.GROUP, at=None, msg=None):
        """
        Called when the client is listening, and somebody removes an admin from a group thread

        :param mid: The action ID
        :param removed_id: The ID of the admin who got removed
        :param author_id: The ID of the person who removed the admins
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        self.log.info("{} removed admin: {} in {}".format(author_id, removed_id, thread_id))

    async def on_approval_mode_change(self, mid=None, approval_mode=None, author_id=None,
                                      thread_id=None, thread_type=ThreadType.GROUP, at=None,
                                      msg=None) -> None:
        """
        Called when the client is listening, and somebody changes approval mode in a group thread

        :param mid: The action ID
        :param approval_mode: True if approval mode is activated
        :param author_id: The ID of the person who changed approval mode
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        if approval_mode:
            self.log.info("{} activated approval mode in {}".format(author_id, thread_id))
        else:
            self.log.info("{} disabled approval mode in {}".format(author_id, thread_id))

    async def on_message_seen(self, seen_by: str = None, thread_id: str = None,
                              thread_type=ThreadType.USER, seen_at: int = None, at: int = None,
                              metadata: Any = None, msg: Any = None) -> None:
        """
        Called when the client is listening, and somebody marks a message as seen

        :param seen_by: The ID of the person who marked the message as seen
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param seen_at: A timestamp of when the person saw the message
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver, thread_type)
        puppet = pu.Puppet.get_by_fbid(seen_by)
        await portal.handle_facebook_seen(self, puppet)

    async def on_message_delivered(self, msg_ids=None, delivered_for=None, thread_id=None,
                                   thread_type=ThreadType.USER, at=None, metadata=None, msg=None
                                   ) -> None:
        """
        Called when the client is listening, and somebody marks messages as delivered

        :param msg_ids: The messages that are marked as delivered
        :param delivered_for: The person that marked the messages as delivered
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "Messages {} delivered to {} in {} ({}) at {}s".format(
                msg_ids, delivered_for, thread_id, thread_type.name, at
            )
        )

    async def on_marked_seen(self, threads=None, seen_at=None, at=None, metadata=None, msg=None
                             ) -> None:
        """
        Called when the client is listening, and the client has successfully marked threads as seen

        :param threads: The threads that were marked
        :param seen_at: A timestamp of when the threads were seen
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        """
        self.log.info(
            "Marked messages as seen in threads {} at {}s".format(
                [(x[0], x[1].name) for x in threads], seen_at
            )
        )

    async def on_message_unsent(self, mid: str = None, author_id: str = None,
                                thread_id: str = None, thread_type: ThreadType = None,
                                at: int = None, msg: Any = None) -> None:
        """
        Called when the client is listening, and someone unsends (deletes for everyone) a message

        :param mid: ID of the unsent message
        :param author_id: The ID of the person who unsent the message
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver, thread_type)
        puppet = pu.Puppet.get_by_fbid(author_id)
        await portal.handle_facebook_unsend(self, puppet, mid)

    async def on_people_added(self, mid=None, added_ids=None, author_id=None, thread_id=None,
                              at=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody adds people to a group thread

        :param mid: The action ID
        :param added_ids: The IDs of the people who got added
        :param author_id: The ID of the person who added the people
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        self.log.info(
            "{} added: {} in {}".format(author_id, ", ".join(added_ids), thread_id)
        )

    async def on_person_removed(self, mid=None, removed_id=None, author_id=None, thread_id=None,
                                at=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody removes a person from a group thread

        :param mid: The action ID
        :param removed_id: The ID of the person who got removed
        :param author_id: The ID of the person who removed the person
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        self.log.info("{} removed: {} in {}".format(author_id, removed_id, thread_id))

    async def on_friend_request(self, from_id=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody sends a friend request

        :param from_id: The ID of the person that sent the request
        :param msg: A full set of the data recieved
        """
        self.log.info("Friend request from {}".format(from_id))

    async def on_inbox(self, unseen=None, unread=None, recent_unread=None, msg=None) -> None:
        """
        .. todo::
            Documenting this

        :param unseen: --
        :param unread: --
        :param recent_unread: --
        :param msg: A full set of the data recieved
        """
        self.log.info("Inbox event: {}, {}, {}".format(unseen, unread, recent_unread))

    async def on_typing(self, author_id=None, status=None, thread_id=None, thread_type=None,
                        msg=None) -> None:
        """
        Called when the client is listening, and somebody starts or stops typing into a chat

        :param author_id: The ID of the person who sent the action
        :param status: The typing status
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(f"User is typing: {author_id} {status} in {thread_id} {thread_type}")

    async def on_game_played(self, mid=None, author_id=None, game_id=None, game_name=None,
                             score=None, leaderboard=None, thread_id=None, thread_type=None,
                             at=None,
                             metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody plays a game

        :param mid: The action ID
        :param author_id: The ID of the person who played the game
        :param game_id: The ID of the game
        :param game_name: Name of the game
        :param score: Score obtained in the game
        :param leaderboard: Actual leaderboard of the game in the thread
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            '{} played "{}" in {} ({})'.format(
                author_id, game_name, thread_id, thread_type.name
            )
        )

    async def on_reaction_added(self, mid: str = None, reaction: MessageReaction = None,
                                author_id: str = None, thread_id: str = None,
                                thread_type: ThreadType = None, at: int = None, msg: Any = None
                                ) -> None:
        """
        Called when the client is listening, and somebody reacts to a message

        :param mid: Message ID, that user reacted to
        :param reaction: Reaction
        :param author_id: The ID of the person who reacted to the message
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type reaction: models.MessageReaction
        :type thread_type: models.ThreadType
        """
        self.log.debug(f"onReactionAdded({mid}, {reaction}, {author_id}, {thread_id}, "
                       f"{thread_type})")
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver, thread_type)
        puppet = pu.Puppet.get_by_fbid(author_id)
        await portal.handle_facebook_reaction_add(self, puppet, mid, reaction.value)

    async def on_reaction_removed(self, mid: str = None, author_id: str = None,
                                  thread_id: str = None, thread_type: ThreadType = None,
                                  at: int = None, msg: Any = None) -> None:
        """
        Called when the client is listening, and somebody removes reaction from a message

        :param mid: Message ID, that user reacted to
        :param author_id: The ID of the person who removed reaction
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.debug(f"onReactionRemoved({mid}, {author_id}, {thread_id}, {thread_type})")
        fb_receiver = self.uid if thread_type == ThreadType.USER else None
        portal = po.Portal.get_by_fbid(thread_id, fb_receiver, thread_type)
        puppet = pu.Puppet.get_by_fbid(author_id)
        await portal.handle_facebook_reaction_remove(self, puppet, mid)

    async def on_block(self, author_id=None, thread_id=None, thread_type=None, at=None, msg=None
                       ) -> None:
        """
        Called when the client is listening, and somebody blocks client

        :param author_id: The ID of the person who blocked
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} blocked {} ({}) thread".format(author_id, thread_id, thread_type.name)
        )

    async def on_unblock(self, author_id=None, thread_id=None, thread_type=None, at=None, msg=None
                         ) -> None:
        """
        Called when the client is listening, and somebody blocks client

        :param author_id: The ID of the person who unblocked
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} unblocked {} ({}) thread".format(author_id, thread_id, thread_type.name)
        )

    async def on_live_location(self, mid=None, location=None, author_id=None, thread_id=None,
                               thread_type=None, at=None, msg=None) -> None:
        """
        Called when the client is listening and somebody sends live location info

        :param mid: The action ID
        :param location: Sent location info
        :param author_id: The ID of the person who sent location info
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        :type location: models.LiveLocationAttachment
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} sent live location info in {} ({}) with latitude {} and longitude {}".format(
                author_id, thread_id, thread_type, location.latitude, location.longitude
            )
        )

    async def on_call_started(self, mid=None, caller_id=None, is_video_call=None, thread_id=None,
                              thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        .. todo::
            Make this work with private calls

        Called when the client is listening, and somebody starts a call in a group

        :param mid: The action ID
        :param caller_id: The ID of the person who started the call
        :param is_video_call: True if it's video call
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} started call in {} ({})".format(caller_id, thread_id, thread_type.name)
        )

    async def on_call_ended(self, mid=None, caller_id=None, is_video_call=None, call_duration=None,
                            thread_id=None, thread_type=None, at=None, metadata=None, msg=None
                            ) -> None:
        """
        .. todo::
            Make this work with private calls

        Called when the client is listening, and somebody ends a call in a group

        :param mid: The action ID
        :param caller_id: The ID of the person who ended the call
        :param is_video_call: True if it was video call
        :param call_duration: Call duration in seconds
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} ended call in {} ({})".format(caller_id, thread_id, thread_type.name)
        )

    async def on_user_joined_call(self, mid=None, joined_id=None, is_video_call=None,
                                  thread_id=None,
                                  thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody joins a group call

        :param mid: The action ID
        :param joined_id: The ID of the person who joined the call
        :param is_video_call: True if it's video call
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} joined call in {} ({})".format(joined_id, thread_id, thread_type.name)
        )

    async def on_poll_created(self, mid=None, poll=None, author_id=None, thread_id=None,
                              thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody creates a group poll

        :param mid: The action ID
        :param poll: Created poll
        :param author_id: The ID of the person who created the poll
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type poll: models.Poll
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} created poll {} in {} ({})".format(
                author_id, poll, thread_id, thread_type.name
            )
        )

    async def on_poll_voted(self, mid=None, poll=None, added_options=None, removed_options=None,
                            author_id=None, thread_id=None, thread_type=None, at=None,
                            metadata=None,
                            msg=None) -> None:
        """
        Called when the client is listening, and somebody votes in a group poll

        :param mid: The action ID
        :param poll: Poll, that user voted in
        :param author_id: The ID of the person who voted in the poll
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type poll: models.Poll
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} voted in poll {} in {} ({})".format(
                author_id, poll, thread_id, thread_type.name
            )
        )

    async def on_plan_created(self, mid=None, plan=None, author_id=None, thread_id=None,
                              thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody creates a plan

        :param mid: The action ID
        :param plan: Created plan
        :param author_id: The ID of the person who created the plan
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type plan: models.Plan
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} created plan {} in {} ({})".format(
                author_id, plan, thread_id, thread_type.name
            )
        )

    async def on_plan_ended(self, mid=None, plan=None, thread_id=None, thread_type=None, at=None,
                            metadata=None, msg=None):
        """
        Called when the client is listening, and a plan ends

        :param mid: The action ID
        :param plan: Ended plan
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type plan: models.Plan
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "Plan {} has ended in {} ({})".format(plan, thread_id, thread_type.name)
        )

    async def on_plan_edited(self, mid=None, plan=None, author_id=None, thread_id=None,
                             thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody edits a plan

        :param mid: The action ID
        :param plan: Edited plan
        :param author_id: The ID of the person who edited the plan
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type plan: models.Plan
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} edited plan {} in {} ({})".format(
                author_id, plan, thread_id, thread_type.name
            )
        )

    async def on_plan_deleted(self, mid=None, plan=None, author_id=None, thread_id=None,
                              thread_type=None, at=None, metadata=None, msg=None) -> None:
        """
        Called when the client is listening, and somebody deletes a plan

        :param mid: The action ID
        :param plan: Deleted plan
        :param author_id: The ID of the person who deleted the plan
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type plan: models.Plan
        :type thread_type: models.ThreadType
        """
        self.log.info(
            "{} deleted plan {} in {} ({})".format(
                author_id, plan, thread_id, thread_type.name
            )
        )

    async def on_plan_participation(self, mid=None, plan=None, take_part=None, author_id=None,
                                    thread_id=None, thread_type=None, at=None, metadata=None,
                                    msg=None) -> None:
        """
        Called when the client is listening, and somebody takes part in a plan or not

        :param mid: The action ID
        :param plan: Plan
        :param take_part: Whether the person takes part in the plan or not
        :param author_id: The ID of the person who will participate in the plan or not
        :param thread_id: Thread ID that the action was sent to. See :ref:`intro_threads`
        :param thread_type: Type of thread that the action was sent to. See :ref:`intro_threads`
        :param at: A timestamp of the action
        :param metadata: Extra metadata about the action
        :param msg: A full set of the data recieved
        :type plan: models.Plan
        :type take_part: bool
        :type thread_type: models.ThreadType
        """
        if take_part:
            self.log.info(
                "{} will take part in {} in {} ({})".format(
                    author_id, plan, thread_id, thread_type.name
                )
            )
        else:
            self.log.info(
                "{} won't take part in {} in {} ({})".format(
                    author_id, plan, thread_id, thread_type.name
                )
            )

    async def on_qprimer(self, at=None, msg=None) -> None:
        """
        Called when the client just started listening

        :param at: A timestamp of the action
        :param msg: A full set of the data recieved
        """
        pass

    async def on_chat_timestamp(self, buddylist: Dict[str, ActiveStatus] = None, msg: Any = None
                                ) -> None:
        """
        Called when the client receives chat online presence update

        :param buddylist: A list of dicts with friend id and last seen timestamp
        :param msg: A full set of the data recieved
        """
        for user, status in buddylist.items():
            puppet = pu.Puppet.get_by_fbid(user, create=False)
            if puppet:
                await puppet.default_mxid_intent.set_presence(
                    presence=PresenceState.ONLINE if status.active else PresenceState.OFFLINE,
                    ignore_cache=True)

    async def on_buddylist_overlay(self, statuses: Dict[str, ActiveStatus] = None, msg: Any = None
                                   ) -> None:
        """
        Called when the client is listening and client receives information about friend active status

        :param statuses: Dictionary with user IDs as keys and :class:`models.ActiveStatus` as values
        :param msg: A full set of the data recieved
        :type statuses: dict
        """
        await self.on_chat_timestamp(statuses, msg)

    async def on_unknown_messsage_type(self, msg: Any = None) -> None:
        """
        Called when the client is listening, and some unknown data was recieved

        :param msg: A full set of the data recieved
        """
        self.log.debug("Unknown message received: {}".format(msg))

    async def on_message_error(self, exception: Exception = None, msg: Any = None) -> None:
        """
        Called when an error was encountered while parsing recieved data

        :param exception: The exception that was encountered
        :param msg: A full set of the data recieved
        """
        self.log.exception("Exception in parsing of {}".format(msg))

    # endregion


def init(context: 'Context') -> Iterable[Awaitable[bool]]:
    global config
    User.az, config, User.loop = context.core
    User._community_helper = CommunityHelper(User.az)
    return (user.load_session() for user in User.get_all())
