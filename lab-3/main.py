#!/usr/bin/env python3
def get_avg(array):
    return sum(int(i) for i in array)/len(array)


def split(line):
    res = line.split(' ')
    return [' '.join(res[0:2]), res[2], res[3],
            ' '.join(res[4:]), get_avg(res[4:])]


def sort(array, col=4, ascending=True):
    return sorted(array, key=lambda val: val[col], reverse=not ascending)


def prnt(line):
    print("%s -> %f" % (' | '.join(line[:4]), line[4]))


if __name__ == '__main__':
    file = "file"
    with open(file, "r") as f:
        result = list(map(lambda line: split(line.rstrip()), f.readlines()))
    result = sort(result, 1, False)
    print(result)
    map(lambda line: prnt(line), result)
