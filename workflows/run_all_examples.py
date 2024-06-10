from utils import Log

from examples import (example_1_from_topojson, example_2_from_ents,
                      example_3_from_ents_by_population, example_4_pds)

log = Log('_run_all_examples')


def main():
    for mod in [
        example_1_from_topojson,
        example_2_from_ents,
        example_3_from_ents_by_population,
        example_4_pds,
    ]:
        log.info(f'Running {mod.__name__}')
        mod.main()


if __name__ == "__main__":
    main()
