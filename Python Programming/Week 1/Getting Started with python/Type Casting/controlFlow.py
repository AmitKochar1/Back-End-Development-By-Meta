
total_bill = 210

discount1 = 10
discount2 = 20

if total_bill >= 100 and total_bill <= 200:
    total_bill = total_bill - discount1
    print('Total Bill is: $' + str(total_bill))
elif total_bill > 200:
    total_bill = total_bill - discount2
    print('Total bill is: $ ' + str(total_bill))
else: print('Total bill is less than $100, Amount to pay: $ ' + str(total_bill))