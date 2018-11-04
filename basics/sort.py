def reverse(num):
    return num*-1

x = sorted([-4,1,-2,3,5,6], key=reverse, reverse=True)
print(x)