class PaySlip:
    def __init__(self, name, payement, amount) -> None:
        self.name = name
        self.payement = payement
        self.amount = amount

    def pay(self):
        self.payement = 'yes'

    def status(self):
        if self.payement == "yes":
            return self.name + " is paid: " + str(self.amount)
        else:
            return self.name + " is not paid."

nathan = PaySlip('Nathan','no', 10000)
print(nathan.status())

nathan.pay()
print('after payement')

print(nathan.status())

