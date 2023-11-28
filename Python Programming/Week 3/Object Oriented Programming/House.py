class House:
    '''
    This is a stub for a class representing a house that can be used to create objects and evaluate different metrics that we may require in constructing it.
    '''
    num_rooms = 5
    bathrooms = 2
    def cost_evaluation(self, rate):
        cost = self.num_rooms * rate
        return cost
        pass
        # Functionality to calculate the costs from the area of the house

house = House()
print(house.cost_evaluation(200))
print(House.cost_evaluation(100))

# house.num_rooms = 7
# print(house.num_rooms)
# print(House.num_rooms)

# House.num_rooms = 9
# print(house.num_rooms)
# print(House.num_rooms)