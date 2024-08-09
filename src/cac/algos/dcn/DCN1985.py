from utils import Log

from cac.algos.dcn.impl import (DCN1985AlgoRunner, DCN1985Base, DCN1985Builder,
                                DCN1985Loader, DCN1985Logger,
                                DCN1985Properties, DCN1985Renderer)

log = Log('DCN1985')


class DCN1985(
    DCN1985Base,
    DCN1985Loader,
    DCN1985AlgoRunner,
    DCN1985Renderer,
    DCN1985Logger,
    DCN1985Properties,
    DCN1985Builder,
):
    pass
