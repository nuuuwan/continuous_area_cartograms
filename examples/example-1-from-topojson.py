import os

from cac import DNC

if __name__ == "__main__":
    file_name = 'Provinces'
    id_field = 'prov_c'

    dnc = DNC.from_topojson(
        os.path.join('topojson', f'{file_name}.json'),
        lambda gdf: gdf[id_field],
        {},
    )

    dnc.run(file_label=f"topojson.{file_name}", n=10)
