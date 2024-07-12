from dataclasses import dataclass


@dataclass
class DCN1985RenderParams:
    # common
    title: str = ''

    # start
    start_value_unit: str = ""
    start_value_hue: int = 120

    # end
    end_value_unit: str = ""
    end_value_hue: int = 240
