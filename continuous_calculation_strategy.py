from abstract_calculation_strategy import AbstractCalculationStrategy

class ContinuousCalculationStrategy(AbstractCalculationStrategy):
    def calculate(self, values):
        return sum(values)
