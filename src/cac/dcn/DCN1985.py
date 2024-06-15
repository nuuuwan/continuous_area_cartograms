from utils import Log

from cac.dcn.DCN1985Base import DCN1985Base
from cac.dcn.DCN1985Loader import DCN1985Loader
from cac.dcn.DCN1985Logger import DCN1985Logger
from cac.dcn.DCN1985Properties import DCN1985Properties
from cac.dcn.DCN1985Renderer import DCN1985Renderer
from cac.dcn.DCN1985RenderHexBin import DCN1985RenderHexBin
from cac.dcn.DCN1985Runner import DCN1985Runner

log = Log('DCN1985')


class DCN1985(
    DCN1985Base,
    DCN1985Loader,
    DCN1985Runner,
    DCN1985Renderer,
    DCN1985RenderHexBin,
    DCN1985Logger,
    DCN1985Properties,
):
    pass
