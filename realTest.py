a = [1,2,3,4,5,6]


def sum(*nums):
    result = 0

    for i in (nums):
        if type(i) is list or tuple:
            for j in i :
                result += j
        if type(i) is int:
            result += i

    return result


print(sum([1,2,3,4,5,6,7,8,9]))
print(sum(a))
