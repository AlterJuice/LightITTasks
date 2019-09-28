
# First Tour LightIT


arr1 = [3, 2, "two", 'apple', 'apple']
arr2 = [3, '3', 2, "two", 'apple', 'apple', 'apple']
# arr3 = [3, 2, "two", 'apple', 'applE']


# def check_array_2(array):  # for any arrays
#     array = [i if isinstance(i, int) else i.lower() for i in array]
#     return any(map(lambda x: array.count(x) % 2 == 0, set(array)))


def check_array(array):
    return any(array.count(x) % 2 == 0 for x in set(i if isinstance(i, int) else i.lower() for i in array))


print(check_array(arr1))  # Must be True
print(check_array(arr2))  # Must be False
print("________________")

# print(check_array_2(arr3))  # Must be True
# print(check_array_2(arr2))  # Must be False

input()
