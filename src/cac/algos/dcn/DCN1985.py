from utils import Log

from cac.algos.dcn.impl import (DCN1985Base, DCN1985Loader, DCN1985Logger,
                                DCN1985Properties, DCN1985Renderer,
                                DCN1985RenderHexBin, DCN1985Runner)

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
