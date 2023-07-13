my_dict = {'x': '2 + 3', 'y': '4 * 5', 'z': '6 - 1'}
for key, value in my_dict.items():
    globals()[key] = eval(value)

# Now you can access the variables x, y, and z
print(x) # 5
print(y) # 20
print(z) # 5