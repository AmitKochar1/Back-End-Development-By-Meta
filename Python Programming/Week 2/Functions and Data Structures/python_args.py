def sum(*args):
    sum = 0
    for x in args:
        sum += x
    return sum


print(sum(1,2,5,8,10))