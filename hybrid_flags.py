from discord.ext.commands import FlagConverter
from discord import Member

class RespectFlags(FlagConverter):
    member: Member

class YnFlags(FlagConverter):
    question: str

class BdayFlags(FlagConverter):
    date: str

class LbFlags(FlagConverter):
    action: str

class GifFlags(FlagConverter):
    user: Member