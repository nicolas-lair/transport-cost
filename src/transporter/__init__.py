import dataclasses

from src.cost_calculator import TotalCostCalculator
from .transporter_params import AbstractTransporterParams


@dataclasses.dataclass
class Transporter:
    cost_calculator: TotalCostCalculator
    transporter_config: AbstractTransporterParams
