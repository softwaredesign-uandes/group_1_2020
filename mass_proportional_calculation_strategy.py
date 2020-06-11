from abstract_calculation_strategy import AbstractCalculationStrategy


class MassProportionalCalculationStrategy(AbstractCalculationStrategy):

    def calculate(self, unit_values, mass_values, denominator, unit):
        multiplier = 1
        if unit == "percentage":
            multiplier = 1
        elif unit == "ppm":
            multiplier = 0.0001
        elif unit == "oz_per_ton":
            multiplier = 0.00342853
        elif unit == "proportion":
            multiplier = 100
        value = sum(sum(mass_values) * (uv * multiplier) for uv in unit_values) / denominator
        return value