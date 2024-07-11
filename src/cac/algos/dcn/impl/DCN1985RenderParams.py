from dataclasses import dataclass


@dataclass
class DCN1985RenderParams:
    title: str = ''
    area_unit: str = "area (%)"
    value_unit: str = "value"
    true_total_area: float = 100
