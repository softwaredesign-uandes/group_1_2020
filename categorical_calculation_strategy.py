from abstract_calculation_strategy import AbstractCalculationStrategy

class CategoricalCalculationStrategy(AbstractCalculationStrategy):
    def calculate(self, values):
        return max(set(values), key=values.count)
