from datetime import date

class Habit:
    def __init__(self, name, frequency="daily"):
        self.name = name
        self.frequency = frequency
        self.created_at = date.today()
