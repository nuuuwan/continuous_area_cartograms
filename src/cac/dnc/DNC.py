from utils import Log

from cac.dnc.DNCBase import DNCBase
from cac.dnc.DNCLoader import DNCLoader
from cac.dnc.DNCLogger import DNCLogger
from cac.dnc.DNCRenderer import DNCRenderer
from cac.dnc.DNCRenderHexBin import DNCRenderHexBin
from cac.dnc.DNCRunner import DNCRunner

log = Log('DNC')


class DNC(
    DNCBase, DNCLoader, DNCRunner, DNCRenderer, DNCRenderHexBin, DNCLogger
):
    pass
