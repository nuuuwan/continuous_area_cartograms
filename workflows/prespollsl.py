import json
import os

from gig import Ent, EntType
from utils import File, JSONFile


def run(ENT_TYPE, EXAMPLE_NAME):
    hexbin_data_path = os.path.join(
        'examples', EXAMPLE_NAME, 'hexbin.svg.json'
    )

    data = JSONFile(hexbin_data_path).read()
    ents = Ent.list_from_type(ENT_TYPE)

    name_to_id = {ent.name: ent.id for ent in ents}

    idx_renamed = {}
    for name, points in data['idx'].items():
        id = name_to_id[name]
        idx_renamed[id] = points[0]
    data['idx'] = idx_renamed

    idx2_norm = {}
    for id, polygons in data['idx2'].items():
        norm_polygons = [
            [[round(x, 2) for x in point] for point in polygon]
            for polygon in polygons
        ]
        idx2_norm[id] = norm_polygons
    data['idx2'] = idx2_norm

    output_path = hexbin_data_path + '.txt'
    File(output_path).write(json.dumps(data, indent=4))
    os.startfile(output_path)


if __name__ == '__main__':
    for [ENT_TYPE, EXAMPLE_NAME] in [
        [EntType.PD, 'lk_pds_in_units'],
        [EntType.ED, 'lk_eds_in_units'],
        [EntType.PROVINCE, 'lk_provinces_in_units'],
    ]:
        run(ENT_TYPE, EXAMPLE_NAME)
