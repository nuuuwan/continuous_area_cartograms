from functools import cache, cached_property
from gig import Ent, EntType, GIGTable

from cac.algos import DCN1985, DCN1985AlgoParams, DCN1985RenderParams 
from cac.extended.MultiStageCAC import MultiStageCAC

class GIGTableMCAC:
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

    def build(self, dir_path: str):
        ents = Ent.list_from_type(self.ent_type)
        algo_params = DCN1985AlgoParams(max_iterations=20)
        dnc_list = []

        ent_lk = Ent.from_id('LK')
        row_lk = ent_lk.gig(self.gig_table)
        fields = list(row_lk.dict.keys())
       
        n = len(fields)
        for i, field in enumerate(fields):
            hue = 300 * i / n
            values = []
            for ent in ents:
                row = ent.gig(self.gig_table)
                values.append(row.dict[field])

            dnc = DCN1985.from_ents(
                ents,
                values,
                algo_params=algo_params,
                render_params=DCN1985RenderParams(
                    title=self.title,
                    end_value_unit=self.format_field(field),
                    end_value_hue=hue,
                ),
            )
            dnc_list.append(dnc)

        MultiStageCAC(*dnc_list).build(dir_path)
