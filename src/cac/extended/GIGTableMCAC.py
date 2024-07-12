from functools import cache, cached_property

from gig import Ent, EntType, GIGTable
from utils import Log

from cac.algos import DCN1985, DCN1985AlgoParams, DCN1985RenderParams
from cac.extended.MultiStageCAC import MultiStageCAC

log = Log('GIGTableMCAC')


class GIGTableMCAC:
    MIN_P = 0.001

    def __init__(self, gig_table: GIGTable, ent_type: EntType):
        self.gig_table = gig_table
        self.ent_type = ent_type

    @cached_property
    def measurement_label(self) -> str:
        return self.gig_table.measurement.replace('_', ' ').title()

    @cached_property
    def entity_label(self) -> str:
        return self.ent_type.name.title()

    @cached_property
    def title(self) -> str:
        return self.measurement_label + " by " + self.entity_label

    @staticmethod
    @cache
    def format_field(field: str) -> str:
        field = field.replace('_', ' ').title()
        for before, after in [('Ind', 'Indian'), ('Sl', 'Sri Lankan')]:
            field = field.replace(before, after)
        return field

    @cached_property
    def fields(self) -> list[str]:
        ent_lk = Ent.from_id('LK')
        row_lk = ent_lk.gig(self.gig_table)
        fields = [
            items[0]
            for items in row_lk.dict_p.items()
            if items[1] > self.MIN_P
        ]
        log.debug(f'{fields=}')
        return fields

    @cached_property
    def algo_params(self) -> DCN1985AlgoParams:
        return DCN1985AlgoParams(max_iterations=40, do_shrink=True)
    

    @staticmethod
    def get_color(field: str) -> str:
        FIELD_TO_COLOR = dict(
            sinhalese='maroon',
            sl_tamil='orange',
            sl_moor='green',
            ind_tamil='orange',
            malay='green',
            burgher='blue',
        )
        return FIELD_TO_COLOR.get(field, 'gray')

    def build(self, dir_path: str):
        ents = Ent.list_from_type(self.ent_type)
        dnc_list = []

        for field in self.fields:
            color = self.get_color(field)
            values = []
            for ent in ents:
                row = ent.gig(self.gig_table)
                values.append(row.dict[field])

            dnc = DCN1985.from_ents(
                ents,
                values,
                algo_params=self.algo_params,
                render_params=DCN1985RenderParams(
                    title=self.title,
                    start_value_color='gray',
                    end_value_unit=self.format_field(field),
                    end_value_color=color,
                ),
            )
            dnc_list.append(dnc)

        MultiStageCAC(*dnc_list).build(dir_path)
