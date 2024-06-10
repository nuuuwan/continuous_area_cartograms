from utils import Log

from cac.dnc.DNCBase import DNCBase
from cac.dnc.DNCLoader import DNCLoader
from cac.dnc.DNCLogger import DNCLogger
from cac.dnc.DNCRenderer import DNCRenderer
from cac.dnc.DNCRunner import DNCRunner

log = Log('DNC')


class DNC(DNCBase, DNCLoader, DNCRunner, DNCRenderer, DNCLogger):
    pass
