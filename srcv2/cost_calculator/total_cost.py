from collections import UserDict

from .constant import CostType
from .abstract_cost import AbstractCost
from .expedition import MultiRefExpedition


class TotalCostCalculator(UserDict[CostType, AbstractCost]):
    def compute_cost(self, gas_factor: float, expedition: MultiRefExpedition, *args, **kwargs):
        total_cost = sum(
            [cc.compute_cost(expedition=expedition,  *args, gas_factor=gas_factor, **kwargs) for cc in self.values()])
        return total_cost
