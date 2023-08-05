from typing import TypedDict, Literal

from clutch.method.typing.torrent.action import IdsArg


class TorrentRenameArguments(TypedDict):
    ids: IdsArg
    path: str
    name: str


class TorrentRenameOptional(TypedDict, total=False):
    tag: int


class TorrentRename(TorrentRenameOptional):
    method: Literal["torrent-rename"]
    arguments: TorrentRenameArguments
