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
from typing import Optional, Dict, Iterator, Iterable, Awaitable, TYPE_CHECKING
import logging
import asyncio
import attr

from fbchat import User as FBUser
from mautrix.types import UserID, RoomID, SyncToken
from mautrix.appservice import AppService, IntentAPI
from mautrix.bridge.custom_puppet import CustomPuppetMixin
from mautrix.util.simple_template import SimpleTemplate

from .config import Config
from .db import Puppet as DBPuppet
from . import user as u, portal as p, matrix as m

if TYPE_CHECKING:
    from .context import Context

config: Config


class Puppet(CustomPuppetMixin):
    log: logging.Logger = logging.getLogger("mau.puppet")
    az: AppService
    loop: asyncio.AbstractEventLoop
    mx: m.MatrixHandler
    hs_domain: str
    mxid_template: SimpleTemplate[str]

    by_fbid: Dict[str, 'Puppet'] = {}
    by_custom_mxid: Dict[UserID, 'Puppet'] = {}

    fbid: str
    name: str
    photo_id: str

    _is_registered: bool

    custom_mxid: UserID
    access_token: str
    _next_batch: SyncToken

    _db_instance: Optional[DBPuppet]

    intent: IntentAPI

    def __init__(self, fbid: str, name: str = "", photo_id: str = "", is_registered: bool = False,
                 custom_mxid: UserID = "", access_token: str = "", next_batch: SyncToken = "",
                 db_instance: Optional[DBPuppet] = None) -> None:
        self.fbid = fbid
        self.name = name
        self.photo_id = photo_id

        self._is_registered = is_registered

        self.custom_mxid = custom_mxid
        self.access_token = access_token
        self._next_batch = next_batch

        self._db_instance = db_instance

        self.default_mxid = self.get_mxid_from_id(fbid)
        self.default_mxid_intent = self.az.intent.user(self.default_mxid)
        self.intent = self._fresh_intent()

        self.log = self.log.getChild(self.fbid)

        self.by_fbid[fbid] = self
        if self.custom_mxid:
            self.by_custom_mxid[self.custom_mxid] = self

    # region DB conversion

    @property
    def db_instance(self) -> DBPuppet:
        if not self._db_instance:
            self._db_instance = DBPuppet(fbid=self.fbid, name=self.name, photo_id=self.photo_id,
                                         matrix_registered=self._is_registered,
                                         custom_mxid=self.custom_mxid, next_batch=self._next_batch,
                                         access_token=self.access_token)
        return self._db_instance

    @classmethod
    def from_db(cls, db_puppet: DBPuppet) -> 'Puppet':
        return Puppet(fbid=db_puppet.fbid, name=db_puppet.name, photo_id=db_puppet.photo_id,
                      is_registered=db_puppet.matrix_registered, custom_mxid=db_puppet.custom_mxid,
                      access_token=db_puppet.access_token, next_batch=db_puppet.next_batch,
                      db_instance=db_puppet)

    def save(self) -> None:
        self.db_instance.edit(name=self.name, photo_id=self.photo_id,
                              matrix_registered=self._is_registered, custom_mxid=self.custom_mxid,
                              access_token=self.access_token)

    @property
    def next_batch(self) -> SyncToken:
        return self._next_batch

    @next_batch.setter
    def next_batch(self, value: SyncToken) -> None:
        self._next_batch = value
        self.db_instance.edit(next_batch=self._next_batch)

    # endregion

    @property
    def is_registered(self) -> bool:
        return self._is_registered or self.is_real_user

    @is_registered.setter
    def is_registered(self, value: bool) -> None:
        self._is_registered = value

    def default_puppet_should_leave_room(self, room_id: RoomID) -> bool:
        portal = p.Portal.get_by_mxid(room_id)
        return portal and portal.fbid != self.fbid

    async def _leave_rooms_with_default_user(self) -> None:
        await super()._leave_rooms_with_default_user()
        # Make the user join all private chat portals.
        await asyncio.gather(*[self.intent.ensure_joined(portal.mxid)
                               for portal in p.Portal.get_all_by_receiver(self.fbid)
                               if portal.mxid], loop=self.loop)

    def intent_for(self, portal: 'p.Portal') -> IntentAPI:
        if portal.fbid == self.fbid:
            return self.default_mxid_intent
        return self.intent

    # region User info updating

    async def update_info(self, source: Optional['u.User'] = None, info: Optional[FBUser] = None,
                          update_avatar: bool = True) -> 'Puppet':
        if not info:
            info = (await source.fetch_user_info(self.fbid))[self.fbid]
        try:
            changed = await self._update_name(info)
            if update_avatar:
                changed = await self._update_photo(info.photo) or changed
            if changed:
                self.save()
        except Exception:
            self.log.exception(f"Failed to update info from source {source.fbid}")
        return self

    @classmethod
    def _get_displayname(cls, info: FBUser) -> str:
        displayname = None
        for preference in config["bridge.displayname_preference"]:
            if getattr(info, preference, None):
                displayname = getattr(info, preference)
        return config["bridge.displayname_template"].format(displayname=displayname,
                                                            **attr.asdict(info))

    async def _update_name(self, info: FBUser) -> bool:
        name = self._get_displayname(info)
        if name != self.name:
            self.name = name
            await self.default_mxid_intent.set_displayname(self.name)
            return True
        return False

    async def _update_photo(self, photo_url: str) -> bool:
        photo_id = p.Portal._get_photo_id(photo_url)
        if photo_id != self.photo_id:
            self.photo_id = photo_id
            if photo_url:
                avatar_uri, _, _ = await p.Portal._reupload_fb_photo(photo_url,
                                                                     self.default_mxid_intent)
            else:
                avatar_uri = ""
            await self.default_mxid_intent.set_avatar_url(avatar_uri)
            return True
        return False

    # endregion
    # region Getters

    @classmethod
    def get_by_fbid(cls, fbid: str, create: bool = True) -> Optional['Puppet']:
        try:
            return cls.by_fbid[fbid]
        except KeyError:
            pass

        db_puppet = DBPuppet.get_by_fbid(fbid)
        if db_puppet:
            return cls.from_db(db_puppet)

        if create:
            puppet = cls(fbid)
            puppet.db_instance.insert()
            return puppet

        return None

    @classmethod
    def get_by_mxid(cls, mxid: UserID, create: bool = True) -> Optional['Puppet']:
        fbid = cls.get_id_from_mxid(mxid)
        if fbid:
            return cls.get_by_fbid(fbid, create)

        return None

    @classmethod
    def get_by_custom_mxid(cls, mxid: UserID) -> Optional['Puppet']:
        try:
            return cls.by_custom_mxid[mxid]
        except KeyError:
            pass

        db_puppet = DBPuppet.get_by_custom_mxid(mxid)
        if db_puppet:
            return cls.from_db(db_puppet)

        return None

    @classmethod
    def get_id_from_mxid(cls, mxid: UserID) -> Optional[str]:
        return cls.mxid_template.parse(mxid)

    @classmethod
    def get_mxid_from_id(cls, fbid: str) -> UserID:
        return UserID(cls.mxid_template.format_full(fbid))

    @classmethod
    def get_all_with_custom_mxid(cls) -> Iterator['Puppet']:
        for db_puppet in DBPuppet.get_all_with_custom_mxid():
            try:
                yield cls.by_fbid[db_puppet.fbid]
            except KeyError:
                pass

            yield cls.from_db(db_puppet)

    # endregion


def init(context: 'Context') -> Iterable[Awaitable[None]]:
    global config
    Puppet.az, config, Puppet.loop = context.core
    Puppet.mx = context.mx
    CustomPuppetMixin.sync_with_custom_puppets = config["bridge.sync_with_custom_puppets"]
    Puppet.hs_domain = config["homeserver"]["domain"]
    Puppet.mxid_template = SimpleTemplate(config["bridge.username_template"], "userid",
                                          prefix="@", suffix=f":{Puppet.hs_domain}", type=str)

    secret = config["bridge.login_shared_secret"]
    Puppet.login_shared_secret = secret.encode("utf-8") if secret else None
    Puppet.login_device_name = "Facebook Messenger Bridge"

    return (puppet.try_start() for puppet in Puppet.get_all_with_custom_mxid())
