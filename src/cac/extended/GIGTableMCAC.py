from functools import cache, cached_property

from gig import Ent, EntType, GIGTable
from utils import Log

from cac.algos import DCN1985, DCN1985AlgoParams, DCN1985RenderParams
from cac.extended.GridCAC import GridCAC

log = Log('GIGTableMCAC')


class GIGTableMCAC:
    MIN_P = 0.001

    def __init__(
        self,
        gig_table: GIGTable,
        ent_type: EntType,
        render_params: DCN1985RenderParams = None,
    ):
        self.gig_table = gig_table
        self.ent_type = ent_type
        self.render_params = render_params or DCN1985RenderParams()

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
    def scales(self) -> list[float]:
        values = []
        ent_lk = Ent.from_id('LK')
        row_lk = ent_lk.gig(self.gig_table)
        for field in self.fields:
            value = row_lk.dict_p[field]
            values.append(value)

        scales = [value / values[0] for value in values]
        log.debug(f'{scales=}')
        return scales

    @cached_property
    def algo_params(self) -> DCN1985AlgoParams:
        return DCN1985AlgoParams(max_iterations=20, do_shrink=True)

    @staticmethod
    def get_color(field: str) -> str:
        FIELD_TO_COLOR = dict(
            # ethnicity
            sinhalese='maroon',
            sl_tamil='orange',
            sl_moor='green',
            ind_tamil='orange',
            malay='green',
            burgher='blue',
            # religion
            buddhist='yellow',
            hindu='orange',
            islam='green',
            roman_catholic='blue',
            other_christian='purple',
        )
        return FIELD_TO_COLOR.get(field, 'gray')

    def build(self, dir_path: str):
        ents = Ent.list_from_type(self.ent_type)
        dnc_list = []

        for scale, field in zip(self.scales, self.fields):
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
                    super_title=self.title,
                    start_value_color='gray',
                    title=self.format_field(field),
                    end_value_color=color,
                    footer_text=self.render_params.footer_text,
                    scale=scale,
                ),
            )
            dnc_list.append(dnc)

        GridCAC([dnc_list]).build(dir_path)
