def sum(**kwargs):
    sum = 0
    for k, v in kwargs.items():
        sum += v
    return round(sum, 2)


print(sum(coffee=2.99, cake=5.50, juice=10.50))