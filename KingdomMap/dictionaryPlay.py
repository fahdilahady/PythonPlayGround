from bisect import bisect_left

def binary_search(a, x, lo=0, hi=None):  # can't use a to specify default for hi
        hi = hi if hi is not None else len(a)  # hi defaults to len(a)   
        pos = bisect_left(a, x, lo, hi)  # find insertion position
        return pos if pos != hi and a[pos] == x else -1  # don't walk off the end

if __name__ == "__main__":
    # newDict = dict()

    # newDict['a'] = 0
    # print(newDict)
    # if 'a' in newDict:
    #     print('key found')
    
    # newDict['a']+=1
    # print(newDict)
   
    data = [('red', 5), ('blue', 1), ('yellow', 8), ('bbrown', 0), ('black', 0)]
    data.sort(key=lambda r: r[1])
    keys = [r[1] for r in data]         # precomputed list of keys
    print(data[bisect_left(keys, 2)])
    x = binary_search(data, ('red', 4))
    print(x)
    x = binary_search(data, ('red', 1))
    print(x)
    x = binary_search(data, ('bbrown', 0))
    print(x)

    