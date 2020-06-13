class AbstractCalculationStrategy:
    def average(self, values):
        return values / len(values)

    def calculate(self, values):
        pass
