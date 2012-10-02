#!/usr/bin/python

import timeit

dictionary={"one":1}


def test1():
    if dictionary.has_key('one'):
        return True
    else:
        return False

def test2():
    if dictionary.has_key('two'):
        return True
    else:
        return False

def test3():
    try:
        dictionary["one"]
        return True
    except:
        return False

def test4():
    try:
        dictionary["two"]
        return True
    except:
        return False

def test5():
    try:
        dictionary["two"]
        return True
    except KeyError:
        return False

def output(name, iterations, seconds):
    print "%s, %s iterations: %s seconds"% (name, iterations, seconds)

if __name__ == '__main__':
    iterations=10000000

    test_1 = timeit.Timer("test1()","from __main__ import test1")
    output("has_key on existing key", iterations, test_1.timeit(number=iterations))

    test_2 = timeit.Timer("test2()","from __main__ import test2")
    output("has_key on non existing key", iterations, test_2.timeit(number=iterations))

    test_3 = timeit.Timer("test3()","from __main__ import test3")
    output("try/except on existing key", iterations, test_3.timeit(number=iterations))

    test_4 = timeit.Timer("test4()","from __main__ import test4")
    output("try/except all on non existing key", iterations, test_4.timeit(number=iterations))

    test_5 = timeit.Timer("test5()","from __main__ import test5")
    output("try/except KeyError on non existing key", iterations, test_5.timeit(number=iterations))
