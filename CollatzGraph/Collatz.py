import matplotlib.pyplot as plt


def collatz_next(num: int):
    if num % 2 == 0:
        return int(num / 2)
    return 3 * num + 1


def collatz_nums(num: int):
    nums = [num]
    while num != 1:
        num = collatz_next(num)
        nums.append(num)
    return nums


def collatz_graph(num: int):
    y = collatz_nums(num)
    x = range(len(y))
    plt.plot(x, y)
    plt.show()


def collatz_graphs(count: int):
    for i in range(1, count+1):
        y = collatz_nums(i)
        x = range(len(y))
        plt.plot(x, y)
    plt.show()


if __name__ == '__main__':
    collatz_graphs(5000)
