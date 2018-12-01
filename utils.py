class RangeContainer:
    def __init__(self, minimum=0, maximum=1):
        self.min = minimum
        self.max = maximum
        self.printed = False

    def __contains__(self, value):
        if type(value) in [list, tuple]:
            for val in value:
                return value < self.min or value > self.max

        return value >= self.min and value <= self.max

    def __iter__(self):
        return self

    def __next__(self):
        if not self.printed:
            self.printed = True
            return f"{self.min} < x < {self.max}"
        else:
            self.printed = False
            raise StopIteration


