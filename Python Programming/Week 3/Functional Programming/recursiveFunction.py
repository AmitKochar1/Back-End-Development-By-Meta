def recursiveFunction(n):
    if n == 1:
        return 1
        print('N at index 1: ', n)
    else:
        print('N at different index: ', n)
        return (n * recursiveFunction(n-1))
    
print(recursiveFunction(1))