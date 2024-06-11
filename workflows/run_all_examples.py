from utils import Log

from examples.example_1_from_topojson import source as example_1_from_topojson
from examples.example_2_from_ents import source as example_2_from_ents
from examples.example_3_from_ents_by_population import \
    source as example_3_from_ents_by_population
from examples.example_4_pds import source as example_4_pds

log = Log('_run_all_examples')


def main():
    for mod in [
        example_1_from_topojson,
        example_2_from_ents,
        example_3_from_ents_by_population,
        example_4_pds,
    ][2:4]:
        log.info(f'Running {mod.__name__}')

        mod.main()


if __name__ == "__main__":
    main()
