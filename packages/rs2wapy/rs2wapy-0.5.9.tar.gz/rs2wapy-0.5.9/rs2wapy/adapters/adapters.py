from __future__ import annotations

import base64
import hashlib
import re
import sys
import threading
import time
from collections import deque
from dataclasses import dataclass
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from typing import List
from typing import Sequence
from typing import Type
from urllib.parse import urlparse
from urllib.parse import urlunparse

import pycurl
from logbook import Logger
from logbook import StreamHandler
from requests import HTTPError

from rs2wapy._version import get_versions
from rs2wapy.models import models
from rs2wapy.parsing import RS2WebAdminResponseParser

StreamHandler(sys.stdout, level="WARNING").push_application()
logger = Logger(__name__)

_version = get_versions()["version"]
USER_AGENT = f"rs2wapy/{_version}"
del get_versions

CURL_USERAGENT = f"curl/{pycurl.version_info()[1]}"

HEADERS_MAX_LEN = 50
POLICIES = ["ACCEPT", "DENY"]
REMEMBER_LOGIN_1M = 2678400

MAP_PREFIX_TO_GAME_TYPE = {
    "VNTE": "ROGame.ROGameInfoTerritories",
    "VNSU": "ROGame.ROGameInfoSupremacy",
    "VNSK": "ROGame.ROGameInfoSkirmish",
    "WWTE": "WWGame.WWGameInfoTerritories",
    "WWSU": "WWGame.WWGameInfoSupremacy",
    "WWSK": "WWGame.WWGameInfoSkirmish",
    "GMTE": "GreenMenMod.GMGameInfoTerritories",
    "GMSU": "GreenMenMod.GMGameInfoSupremacy",
    "GMSK": "GreenMenMod.GMGameInfoSkirmish",
}

WEB_ADMIN_BASE_PATH = Path("/ServerAdmin/")
WEB_ADMIN_CURRENT_GAME_PATH = WEB_ADMIN_BASE_PATH / Path("current/")
WEB_ADMIN_CHAT_PATH = WEB_ADMIN_CURRENT_GAME_PATH / Path("chat/")
WEB_ADMIN_CHAT_DATA_PATH = WEB_ADMIN_CHAT_PATH / Path("data/")
WEB_ADMIN_ACCESS_POLICY_PATH = WEB_ADMIN_BASE_PATH / Path("policy/")
WEB_ADMIN_CHANGE_MAP_PATH = WEB_ADMIN_CURRENT_GAME_PATH / Path("change/")
WEB_ADMIN_CHANGE_MAP_DATA_PATH = WEB_ADMIN_CHANGE_MAP_PATH / Path("data/")
WEB_ADMIN_PLAYERS_PATH = WEB_ADMIN_CURRENT_GAME_PATH / Path("players/")


def _in(el: object, seq: Sequence[Sequence]) -> bool:
    """Check if element is in any sequence of sequences."""
    for s in seq:
        if el in s:
            return True
    return False


def _read_encoding(headers: dict, index: int = -1) -> str:
    encoding = None
    if "content-type" in headers:
        content_type = headers["content-type"][index].lower()
        match = re.search(r"charset=(\S+)", content_type)
        if match:
            encoding = match.group(1)
            logger.debug("encoding is {enc}", enc=encoding)
    if encoding is None:
        # Default encoding for HTML is iso-8859-1.
        # Other content types may have different default encoding,
        # or in case of binary data, may have no encoding at all.
        encoding = "iso-8859-1"
        logger.debug("assuming encoding is {enc}", enc=encoding)
    return encoding


def _set_postfields(curl_obj: pycurl.Curl, postfields: str):
    postfieldsize = len(postfields)
    logger.debug("postfieldsize: {pf_size}", pf_size=postfieldsize)
    logger.debug("postfields: {pf}", pf=postfields)
    curl_obj.setopt(curl_obj.POSTFIELDS, postfields)
    curl_obj.setopt(curl_obj.POSTFIELDSIZE_LARGE, postfieldsize)


def _policies_to_delete_argstr(policies: List[str], to_delete: str) -> str:
    del_index = [idx for idx, s in enumerate(policies) if to_delete in s][0]
    policies = [p.split(":") for p in policies]
    policies = [(f"ipmask={p[0].strip()}&policy={p[1].strip()}"
                 f"{f'&delete={del_index}' if p[0] == to_delete else ''}")
                for p in policies]
    return "&".join(policies)


def _prepare_headers(headers: dict) -> list:
    """
    Convert headers dictionary to list for PycURL.
    """
    return [f"{key}: {value}" for key, value in headers.items()]


@dataclass
class AuthData:
    timeout: float
    timeout_start: float
    authcred: str
    sessionid: str
    authtimeout: str

    def __post_init__(self):
        if self.timeout < 0:
            raise ValueError(
                f"cannot calculate authentication timeout for timeout: {self.timeout}")

    def timed_out(self) -> bool:
        time_now = time.time()
        if (self.timeout_start + self.timeout) < time_now:
            logger.debug(
                "authentication timed out for start_time={s}, "
                "timeout={t}, time_now={tn}", s=self.timeout_start,
                t=self.timeout, tn=time_now)
            return True
        return False


class WebAdminAdapter:
    BASE_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.7,fi;q=0.3",
        "DNT": 1,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": 1,
        "Referer": "",
    }

    def __init__(self, username: str, password: str, webadmin_url: str):
        self._headers = {}
        self._username = username
        self._webadmin_url = webadmin_url
        self._password_hash = ""
        self._hash_alg = ""
        self._auth_data = None
        self._chat_message_deque = deque(maxlen=512)
        self._rparser = RS2WebAdminResponseParser(
            encoding=_read_encoding(self._headers))

        scheme, netloc, path, params, query, fragment = urlparse(self._webadmin_url)
        logger.debug("webadmin_url={url}, scheme={scheme}, netloc={netloc}, "
                     "path={path}, params={params}, query={query}, fragment={fragment}",
                     url=self._webadmin_url, scheme=scheme, netloc=netloc,
                     path=path, params=params, query=query, fragment=fragment)

        if (not path) or (path == "/"):
            path = WEB_ADMIN_BASE_PATH.as_posix()
        if not path.endswith("/"):
            path = f"{path}/"

        referer = ""
        if not scheme and not netloc:
            referer = path
        elif netloc:
            referer = netloc

        if not referer:
            logger.warning("unable to set 'Referer' in headers")
        else:
            self.BASE_HEADERS["Referer"] = referer
            logger.debug("setting 'Referer' to '{r}'", r=referer)

        self._webadmin_url = urlunparse(
            (scheme, netloc, path, params, query, fragment)
        )
        self._chat_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_CHAT_PATH.as_posix(),
             params, query, fragment)
        )
        self._chat_data_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_CHAT_DATA_PATH.as_posix(),
             params, query, fragment)
        )
        self._current_game_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_CURRENT_GAME_PATH.as_posix(),
             params, query, fragment)
        )
        self._access_policy_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_ACCESS_POLICY_PATH.as_posix(),
             params, query, fragment)
        )
        self._change_map_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_CHANGE_MAP_PATH.as_posix(),
             params, query, fragment)
        )
        self._change_map_data_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_CHANGE_MAP_DATA_PATH.as_posix(),
             params, query, fragment)
        )
        self._players_url = urlunparse(
            (scheme, netloc, WEB_ADMIN_PLAYERS_PATH.as_posix(),
             params, query, fragment)
        )

        self._set_password_hash(username, password)
        self._authenticate()

        self._stop_event = threading.Event()
        self._chat_message_thread = threading.Thread(
            target=self._enqueue_chat_messages, daemon=True)
        self._chat_message_thread.start()

    def __del__(self):
        if self._stop_event:
            self._stop_event.set()

    @property
    def auth_data(self) -> AuthData:
        return self._auth_data

    @auth_data.setter
    def auth_data(self, auth_data: AuthData):
        self._auth_data = auth_data

    @property
    def _pw_hash(self) -> str:
        return base64.decodebytes(self._password_hash).decode("utf-8")

    @_pw_hash.setter
    def _pw_hash(self, pw_hash: str):
        self._password_hash = base64.encodebytes(pw_hash.encode("utf-8"))

    def get_current_game(self) -> models.CurrentGame:
        headers = self._make_auth_headers()
        c = pycurl.Curl()
        resp = self._perform(self._current_game_url, curl_obj=c, headers=headers)
        return self._rparser.parse_current_game(resp)

    def get_chat_messages(self) -> Sequence[models.ChatMessage]:
        """When the Adapter instance is created, it begins polling the
        RS2 WebAdmin server for chat messages, appending them to an internal
        queue. Calling this method pops and returns the messages from
        the internal queue.
        """
        chat_msgs = []
        while True:
            try:
                chat_msgs.append(self._chat_message_deque.popleft())
            except IndexError:
                break
        return chat_msgs

    def post_chat_message(self, message: str, team: Type[models.Team]):
        """Post chat message to RS2 WebAdmin server.
        """
        headers = self._make_chat_headers()
        # noinspection PyTypeChecker
        team_code = {
            models.AllTeam: "-1",
            models.RedTeam: "0",
            models.BlueTeam: "1",
        }[team]

        postfields = f"ajax=1&message={message}&teamsay={team_code}"
        c = pycurl.Curl()
        _set_postfields(c, postfields)

        resp = self._perform(self._chat_data_url, curl_obj=c, headers=headers)

        chat_msgs = self._rparser.parse_chat_messages(resp)
        logger.debug("got {clen} chat messages", clen=len(chat_msgs))
        self._chat_message_deque.extend(chat_msgs)

    def get_access_policy(self) -> List[str]:
        sessionid = self._auth_data.sessionid
        authcred = self._auth_data.authcred
        authtimeout = self._auth_data.authtimeout

        headers = self.BASE_HEADERS.copy()
        headers["Cookie"] = f"{sessionid}; {authcred}; {authtimeout}"
        headers["Cache-Control"] = "no-cache"

        # Prevent caching with randomized parameter.
        url = f"{self._access_policy_url}?$(date +%s)"

        c = pycurl.Curl()
        resp = self._perform(url, curl_obj=c, headers=headers)
        return self._rparser.parse_access_policy(resp)

    def add_access_policy(self, ip_mask: str, policy: str) -> bool:
        """
        Add IP access policy.

        :param ip_mask:
            IP mask of the policy to be added.
        :param policy:
            "DENY" or "ACCEPT".
        :return:
            True if policy added, else False.
        """
        policies = self.get_access_policy()
        if _in(ip_mask, policies):
            logger.info("{ip} already in policies", ip=ip_mask)
            return False

        policy = policy.upper()
        if policy not in POLICIES:
            raise ValueError(f"invalid policy: {policy}")

        action = "add"

        headers = self.BASE_HEADERS.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        max_retries = 10
        retries = 0

        # WORKAROUND:
        # There is an issue where the policy is not always added
        # even though the request is seemingly valid, but repeating
        # the request eventually successfully adds the policy.
        while not _in(ip_mask, policies) and (retries < max_retries):
            headers["Cookie"] = self._find_sessionid()

            postfields = f"action={action}&ipmask={ip_mask}&policy={policy}"

            c = pycurl.Curl()
            _set_postfields(c, postfields)

            try:
                self._perform(self._access_policy_url, curl_obj=c, headers=headers)
            except Exception as e:
                logger.error(e, exc_info=True)

            policies = self.get_access_policy()
            retries += 1

        if retries >= max_retries:
            logger.error("failed to add policy {p}, max retries exceeded", p=ip_mask)
            return False
        return True

    def delete_access_policy(self, ip_mask: str) -> bool:
        """
        Delete IP access policy.

        :param ip_mask:
            IP mask of the access policy to be deleted.
        :return:
            True if deleted, else False.
        """
        policies = self.get_access_policy()
        if ip_mask not in policies:
            logger.info("{ip} not in policies, no need to delete", ip=ip_mask)
            return False

        action = "modify"

        headers = self.BASE_HEADERS.copy()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Accept-Encoding"] = "gzip, deflate"

        max_retries = 10
        retries = 0

        # WORKAROUND:
        # There is an issue where the policy is not always deleted
        # even though the request is seemingly valid, but repeating
        # the request eventually successfully deletes the policy.
        while _in(ip_mask, policies) and (retries < max_retries):
            headers["Cookie"] = self._find_sessionid()

            try:
                argstr = _policies_to_delete_argstr(policies, ip_mask)
            except IndexError as ie:
                logger.error("error finding index of {ipm}: {e}", ipm=ip_mask, e=ie)
                continue

            postfields = f"action={action}&{argstr}"

            c = pycurl.Curl()
            _set_postfields(c, postfields)

            try:
                self._perform(self._access_policy_url, curl_obj=c, headers=headers)
            except Exception as e:
                logger.error(e, exc_info=True)

            policies = self.get_access_policy()
            retries += 1

        if retries >= max_retries:
            logger.error("failed to delete policy {p}, max retries exceeded", p=ip_mask)
            return False
        return True

    def modify_access_policy(self, ip_mask: str, policy: str) -> bool:
        pass

    def change_map(self, new_map: str, url_extra: dict = None):
        if new_map.lower() not in [m.lower() for m in self.get_maps()]:
            logger.warning("{nm} not in server map list", nm=new_map)

        if url_extra is None:
            url_extra = {}

        url_extra_str = ""
        for key, value in url_extra.items():
            url_extra_str += f'"%"3F{key}"%"3D{value}'

        headers = self._make_auth_headers()
        headers["Accept"] = ("text/html,application/xhtml+xml,"
                             "application/xml;q=0.9,image/webp,*/*;q=0.8")
        headers["Cache-Control"] = "max-age=0"

        c_get = pycurl.Curl()
        resp = self._perform(self._change_map_url, curl_obj=c_get, headers=headers)
        mutator_group_count = self._rparser.parse_mutator_group_count(resp)

        map_prefix = new_map.split("-")[0]
        game_type = MAP_PREFIX_TO_GAME_TYPE[map_prefix]

        postfields = (f'gametype={game_type}'
                      f'&map={new_map}'
                      f'&mutatorGroupCount={mutator_group_count}'
                      f'&urlextra={url_extra_str}'
                      f'&action=change')

        headers["Content-Type"] = "application/x-www-form-urlencoded"
        c_post = pycurl.Curl()
        _set_postfields(c_post, postfields)
        self._perform(self._change_map_url, curl_obj=c_post, headers=headers)

    def get_maps(self) -> dict:
        headers = self._make_auth_headers()
        c = pycurl.Curl()
        resp = self._perform(self._change_map_url, curl_obj=c, headers=headers)
        game_type_options = self._rparser.parse_game_type_options(resp)

        headers = self._make_auth_headers()
        headers["Accept"] = ("text/html,application/xhtml+xml,"
                             "application/xml;q=0.9,image/webp,*/*;q=0.8")
        headers["Cache-Control"] = "max-age=0"
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        maps = {}

        for gto in game_type_options:
            postfields = f"ajax=1&gametype={gto}"
            c = pycurl.Curl()
            _set_postfields(c, postfields)
            resp = self._perform(
                self._change_map_data_url, curl_obj=c, headers=headers)
            maps[gto] = self._rparser.parse_map_options(resp)

        return maps

    def get_players(self) -> List[PlayerWrapper]:
        headers = self._make_auth_headers()
        c = pycurl.Curl()
        resp = self._perform(self._players_url, curl_obj=c, headers=headers)
        players = self._rparser.parse_players(resp, adapter=self)
        return players

    def kick_player(self, player: models.Player, reason: str, duration: str):
        raise NotImplementedError

    def ban_player(self, player: models.Player, reason: str, duration: str):
        # --data 'action=banid&playerid=256&playerkey=256_0x0110000103A3105D_107.1604&__Submitter=
        # &__UniqueId=&__PlayerName=&__Reason=testban&__NotifyPlayers=1&__PickList_Length=4
        # &__PickList_0=Disturbing+the+server&__PickList_1=Inappropriate+language
        # &__PickList_2=Insulting+other+player%28s%29&__PickList_3=Insulting+the+admin
        # &__IdType=0&__ExpNumber=1&__ExpUnit=Hour'
        raise NotImplementedError

    def session_ban_player(self, player: models.Player, reason: str):
        raise NotImplementedError

    def _enqueue_chat_messages(self):
        while True and not self._stop_event.is_set():
            self._chat_message_deque.extend(
                self._get_chat_messages_from_server())
            self._stop_event.wait(timeout=2 - time.time() % 2)

    def _get_chat_messages_from_server(self) -> Sequence[models.ChatMessage]:
        headers = self._make_chat_headers()
        postfields = "ajax=1"
        c = pycurl.Curl()
        _set_postfields(c, postfields)
        resp = self._perform(self._chat_data_url, curl_obj=c, headers=headers)
        chat_msgs = self._rparser.parse_chat_messages(resp)
        logger.debug("got {clen} chat messages", clen=len(chat_msgs))
        return chat_msgs

    def _perform(self, url: str, curl_obj: pycurl.Curl = None,
                 headers: dict = None, skip_auth=False) -> bytes:
        if not skip_auth:
            self._wait_authenticated()

        if not curl_obj:
            curl_obj = pycurl.Curl()

        logger.debug("url={url}, headers={headers}", url=url, headers=headers)
        if not headers:
            headers = self.BASE_HEADERS
        headers = _prepare_headers(headers)

        logger.debug("prepared headers={h}", h=headers)

        buffer = BytesIO()

        curl_obj.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl_obj.setopt(pycurl.HEADERFUNCTION, self._header_function)
        curl_obj.setopt(pycurl.BUFFERSIZE, 102400)
        curl_obj.setopt(pycurl.URL, url)
        curl_obj.setopt(pycurl.HTTPHEADER, headers)
        curl_obj.setopt(pycurl.USERAGENT, CURL_USERAGENT)
        curl_obj.setopt(pycurl.MAXREDIRS, 50)
        curl_obj.setopt(pycurl.ACCEPT_ENCODING, "")
        curl_obj.setopt(pycurl.TCP_KEEPALIVE, 1)
        curl_obj.setopt(pycurl.FOLLOWLOCATION, True)
        curl_obj.setopt(pycurl.ENCODING, "gzip, deflate")

        curl_obj.perform()

        status = curl_obj.getinfo(pycurl.HTTP_CODE)
        logger.debug("HTTP status: {s}", s=status)
        curl_obj.close()

        if not status == HTTPStatus.OK:
            logger.error("HTTP status error: {s}", s=status)
            raise HTTPError(self._webadmin_url, status, "error connecting to WebAdmin",
                            fp=None, hdrs=None)

        value = b""
        try:
            value = buffer.getvalue()
        except pycurl.error as e:
            logger.error("error on url={u}, error={e}", u=url, e=e)

        return value

    def _header_function(self, header_line):
        if "connection" in self._headers:
            try:
                if len(self._headers["connection"]) > HEADERS_MAX_LEN:
                    logger.debug("Headers 'connection' values max length ({le}) exceeded, "
                                 "resetting headers (preserving latest entries)",
                                 le=HEADERS_MAX_LEN)
                    new_headers = {}
                    for k, v in self._headers.items():
                        new_headers[k] = v[-1]
                    self._headers = new_headers
                    logger.debug("Headers 'connection' {t} new length={le}",
                                 t=type(self._headers["connection"]),
                                 le=len(self._headers["connection"]))
            except (KeyError, IndexError) as e:
                logger.error("error: {e}", e=e, exc_info=True)

        # HTTP standard specifies that headers are encoded in iso-8859-1.
        header_line = header_line.decode("iso-8859-1")

        # Header lines include the first status line (HTTP/1.x ...).
        # We are going to ignore all lines that don't have a colon in them.
        # This will botch headers that are split on multiple lines...
        if ":" not in header_line:
            return

        # Break the header line into header name and value.
        name, value = header_line.split(":", 1)

        # Remove whitespace that may be present.
        # Header lines include the trailing newline, and there may be whitespace
        # around the colon.
        name = name.strip()
        value = value.strip()

        # Header names are case insensitive.
        # Lowercase name here.
        name = name.lower()

        if name in self._headers:
            if isinstance(self._headers[name], list):
                self._headers[name].append(value)
            else:
                self._headers[name] = [self._headers[name], value]
        else:
            self._headers[name] = value

    def _find_sessionid(self) -> str:
        """
        Find latest session ID in headers.
        """
        # 'sessionid="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
        r = ""
        try:
            if type(self._headers["set-cookie"]) == str:
                logger.debug("type(self._headers['set-cookie']) == str")
                r = re.search(r'sessionid="(.*?)"', self._headers["set-cookie"]).group(1)
            elif type(self._headers["set-cookie"]) == list:
                logger.debug("type(self._headers['set-cookie']) == list")
                sessionid_match = [
                    i for i in self._headers["set-cookie"]
                    if i.startswith("sessionid=")][-1]
                logger.debug("sessionid_match: {si}", si=sessionid_match)
                r = re.search(r'sessionid="(.*?)"', sessionid_match).group(1)
            else:
                logger.error(
                    "type(_headers['set-cookie']) == {t}", t=type(self._headers["set-cookie"]))
                logger.error("cant get sessionid from headers")
                return r
        except AttributeError as ae:
            logger.error("error: {e}", e=ae)
            return r
        except Exception as e:
            logger.error("error: {e}", e=e, exc_info=True)
            return r

        return f'sessionid="{r}";'

    def _post_login(self, sessionid: str, token: str,
                    remember=REMEMBER_LOGIN_1M) -> bytes:
        headers = self.BASE_HEADERS.copy()
        headers["Cookie"] = sessionid
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        postfields = (f"token={token}&password_hash=%24sha1%24{self._pw_hash}"
                      + f"&username={self._username}&password=&remember={remember}")

        c = pycurl.Curl()
        _set_postfields(c, postfields)
        return self._perform(self._webadmin_url, curl_obj=c,
                             headers=headers, skip_auth=True)

    def _authenticate(self):
        resp = self._perform(self._webadmin_url, skip_auth=True)
        if not resp:
            logger.error("no response content from url={url}", url=self._webadmin_url)
            return

        parsed_html = self._rparser.parse_html(resp)
        token = ""
        try:
            token = parsed_html.find("input", attrs={"name": "token"}).get("value")
            logger.debug("token: {token}", token=token)
        except AttributeError as ae:
            logger.error("unable to get token: {e}", e=ae)

        sessionid = self._find_sessionid()
        logger.debug("got sessionid: {si}, from headers", si=sessionid)

        self._post_login(sessionid=sessionid, token=token)

        try:
            authcred = [
                i for i in self._headers["set-cookie"]
                if i.startswith("authcred=")][-1]
            authtimeout = [
                i for i in self._headers["set-cookie"]
                if i.startswith("authtimeout=")][-1]
        except IndexError as ie:
            logger.error("unable to get auth data from headers: {e}", e=ie)
            raise

        authtimeout_value = int(re.search(r'authtimeout="(.*?)"', authtimeout).group(1))

        logger.debug("authcred: {ac}", ac=authcred)
        logger.debug("authtimeout: {ato}", ato=authtimeout)
        logger.debug("authtimeout_value: {ato_value}", ato_value=authtimeout_value)

        self._auth_data = AuthData(
            timeout=authtimeout_value,
            authcred=authcred,
            sessionid=sessionid,
            timeout_start=time.time(),
            authtimeout=authtimeout
        )

    def _wait_authenticated(self):
        if self._auth_data.timed_out():
            self._authenticate()

    def _make_auth_headers(self) -> dict:
        sessionid = self._auth_data.sessionid
        authcred = self._auth_data.authcred
        authtimeout = self._auth_data.authtimeout
        headers = self.BASE_HEADERS.copy()
        headers["Cookie"] = f"{sessionid}; {authcred}; {authtimeout}"
        return headers

    def _make_chat_headers(self) -> dict:
        headers = self._make_auth_headers()
        headers["X-Requested-With"] = "XMLHttpRequest"
        headers["Accept"] = "*/*"
        return headers

    def _set_password_hash(self, username: str, password: str):
        c = pycurl.Curl()
        resp = self._perform(self._webadmin_url, curl_obj=c, skip_auth=True)
        self._hash_alg = self._rparser.parse_hash_alg(resp)
        logger.debug("using hash algorithm: '{a}'", a=self._hash_alg)
        if self._hash_alg:
            self._pw_hash = self._ue3_pw_hash_digest(username, password)
        else:
            # Hash algorithm was not set.
            self._pw_hash = password

    def _ue3_pw_hash_digest(self, username: str, password: str) -> str:
        """
        Calculate the hex digest used by Unreal Engine 3 WebAdmin,
        which is transmitted over the wire.
        """
        hash_alg = getattr(hashlib, self._hash_alg)
        return hash_alg(bytearray(password, "utf-8")
                        + bytearray(username, "utf-8")).hexdigest()


class PlayerWrapper:
    """Wrapper around models.Player, providing functionality
    via WebAdminAdapter.
    """

    def __init__(self, player: models.Player, adapter: WebAdminAdapter):
        self._player = player
        self._adapter = adapter

    def __str__(self) -> str:
        return self._player.__str__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    @property
    def player(self) -> models.Player:
        return self._player

    def ban(self, reason: str, duration: str):
        self._adapter.ban_player(self.player, reason, duration)

    def kick(self, reason: str, duration: str):
        self._adapter.kick_player(self.player, reason, duration)

    def session_ban(self, reason: str):
        self._adapter.session_ban_player(self.player, reason)

    def revoke_ban(self):
        raise NotImplementedError

    def revoke_session_ban(self):
        raise NotImplementedError

    def track(self):
        raise NotImplementedError

    def untrack(self):
        raise NotImplementedError
