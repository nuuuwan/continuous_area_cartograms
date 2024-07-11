from dataclasses import dataclass


@dataclass
class DCN1985RenderParams:
    # common
    title: str = ''
    start_value_unit: str = "area (%)"
    end_value_unit: str = "value"
    start_total_value: float = 100
