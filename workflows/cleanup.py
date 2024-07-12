import os
import shutil

from utils import Log

log = Log('cleanup')


def main():
    DIR_EXAMPLES = 'examples'
    for child_dir_name in os.listdir(DIR_EXAMPLES):
        dir_output_path = os.path.join(DIR_EXAMPLES, child_dir_name, 'output')

        dir_image_path = os.path.join(dir_output_path, 'images')
        shutil.rmtree(dir_image_path)
        log.warning(f'Deleted "{dir_image_path}"')

        dir_geojson_path = os.path.join(dir_output_path, 'geojson')
        shutil.rmtree(dir_geojson_path)
        log.warning(f'Deleted "{dir_geojson_path}"')

        source_py_path = os.path.join(
            DIR_EXAMPLES, child_dir_name, '__main__.py'
        )
        new_main_py_path = os.path.join(
            DIR_EXAMPLES, child_dir_name, '__main__.py'
        )
        shutil.move(source_py_path, new_main_py_path)
        log.warning(f'Moved "{source_py_path}" to "{new_main_py_path}"')

        log.info(f'✅ Cleaned up "{child_dir_name}"')


if __name__ == "__main__":
    main()
