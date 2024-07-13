from dataclasses import dataclass


@dataclass
class DCN1985AlgoParams:
    preprocess_tolerance: float = 0.001
    min_log2_error: float = 0.1
    max_iterations: int = 20
    do_shrink: bool = False
    min_p_area: float = 0.01
