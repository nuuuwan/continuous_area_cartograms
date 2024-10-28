import os
import shutil

from utils import Log

log = Log("build_examples")


class Example:
    DIR_PATH_BASE = "examples"

    def __init__(self, dir_path):
        self.dir_path = dir_path

    @staticmethod
    def list():
        for child in os.listdir(Example.DIR_PATH_BASE):
            child_path = os.path.join(Example.DIR_PATH_BASE, child)
            if os.path.isdir(child_path):
                yield Example(child_path)

    def clean(self):
        for child in os.listdir(self.dir_path):
            child_path = os.path.join(self.dir_path, child)
            if child in ["__main__.py"]:
                continue
            if os.path.isdir(child_path):
                shutil.rmtree(child_path)
                log.debug(f"Removed directory: {child_path}")
            else:
                os.remove(child_path)
                log.debug(f"Removed file: {child_path}")
        log.info(f"Cleaned example: {self.dir_path}")

    def run(self):
        log.info(f"Running example: {self.dir_path}")
        os.system(f"python {self.dir_path}")


def main():
    for example in Example.list():
        example.clean()
        try:
            example.run()
        except Exception as e:
            log.error(f"Failed to run example: {example.dir_path}")
            log.error(e)


if __name__ == "__main__":
    main()
