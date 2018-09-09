import random


def binary_search(dataset, find_num):  # 只能实现查找功能，不能返回下标
    if len(dataset) > 1:
        mid = int(len(dataset) / 2)
        if dataset[mid] == find_num:
            #print("Find it")
            return dataset[mid]
        elif dataset[mid] > find_num:
            return binary_search(dataset[0:mid], find_num)
        else:
            return binary_search(dataset[mid + 1:], find_num)
    else:
        if dataset[0] == find_num:
            #print("Find it")
            return dataset[0]
        else:
            pass
            #print("Cannot find it.")


def quick_search(data_list, val):
    low = 0
    high = len(data_list) - 1
    while low <= high:
        mid = (low + high)//2
        if data_list[mid]["id"] == val:
            return mid, data_list[mid]
        elif data_list[mid]["id"] > val:
            high = mid - 1
        else:
            low = mid + 1
    return


def random_list(n):
    result = []
    # dic = {}
    ids = list(range(1001,1001+n))
    a1 = ['zhao','qian','sun','li']
    a2 = ['li','hao','','']
    a3 = ['qiang','guo']
    for i in range(n):
        # dic = {}  # 定义在里面都没事
        # dic['age'] = random.randint(18,26)
        # dic['id'] = ids[i]
        # dic['name'] = random.choice(a1)+random.choice(a2)+random.choice(a3)
        # 这种写法为什么到最后，列表中全是重复的字典？因为你把字典定义在了外面，每循环一次，都会改变dic的值，

        age = random.randint(18,30)
        id_nu = ids[i]
        name = random.choice(a1)+random.choice(a2)+random.choice(a3)
        dic = {"id": id_nu, "name": name, "age": age}
        # print("dict:", dic)
        result.append(dic)
    return result


def test1(li):
    for j in range(len(li)-1):
        if li[j] > li[j + 1]:
            li[j], li[j + 1] = li[j + 1], li[j]

        print(li)


def quick_sort_x(data, left, right):
    if left < right:
        mid = partition(data, left, right)
        quick_sort_x(data, left, mid - 1)
        quick_sort_x(data, mid + 1, right)


def partition(data, left, right):
    tmp = data[left]
    while left < right:
        while left < right and data[right] >= tmp:
            right -= 1
        data[left] = data[right]
        print("把小的数移到左边", data)
        while left < right and data[left] <= tmp:
            left += 1
        data[right] = data[left]
        print("把大的数移到右边", data)
    data[left] = tmp
    print("退出时的data:", left,data)
    return left

data = [1,2,3,4,5,7,9,11,13,15]
# print(quick_search(random_list(100), 1022))

# li = [2,3,5,1,6,9,7,8,4]
li = [5,7,4,6,3,1,2,9,8]
quick_sort_x(li,0,len(li) - 1)
