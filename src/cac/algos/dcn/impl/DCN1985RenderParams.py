from dataclasses import dataclass


@dataclass
class DCN1985RenderParams:
    # common
    title: str = ''
    start_value_unit: str = "area (%)"
    start_total_value: float = 100
    end_value_unit: str = "value"
    