from dataclasses import dataclass


@dataclass
class DCN1985RenderParams:
    # common
    title: str = ''

    # start
    start_value_unit: str = ""
    start_value_color: str = 'green'

    # end
    end_value_unit: str = ""
    end_value_color: str = 'red'
