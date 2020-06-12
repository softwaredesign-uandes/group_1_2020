from categorical_calculation_strategy import CategoricalCalculationStrategy
from continuous_calculation_strategy import ContinuousCalculationStrategy
from mass_proportional_calculation_strategy import MassProportionalCalculationStrategy

class ReblockAttributeCalculationFactory:
    def strategy(self, category):
        if category == "continuous":
            return ContinuousCalculationStrategy()
        if category == "proportional":
            return MassProportionalCalculationStrategy()
        if category == "categorical":
            return CategoricalCalculationStrategy()
