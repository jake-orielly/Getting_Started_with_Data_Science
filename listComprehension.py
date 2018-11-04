increasing_pairs = [(x,y)
    for x in range(5)
    for y in range(x+1,5)]

even_numbers = [x for x in range(10) if x % 2 == 0]

print(increasing_pairs)
print(even_numbers)