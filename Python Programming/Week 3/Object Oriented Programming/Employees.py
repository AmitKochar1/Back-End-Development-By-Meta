class Employees:
    def __init__(self, name, initial) -> None:
        self.name = name
        self.initial = initial

class Supervisior(Employees):
    def __init__(self, name, initial, password) -> None:
        super().__init__(name, initial)
        self.password = password

class Chefs(Employees):

    def leave(self, days):
        return "May I request: " + str(days) + " days"

nathan = Supervisior("Nathan", "NK", "Apple")

print(nathan.password)

emily = Chefs("Emily", "EP")
print(emily.leave(3))