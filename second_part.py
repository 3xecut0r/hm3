from time import time
import logging
import multiprocessing
import os


def factorize(*number):
    # YOUR CODE HERE
    # (128, 255, 99999, 10651060)
    result = []
    for num in number:
        factors = []
        for el in range(1, num + 1):
            if num % el == 0:
                factors.append(el)
        result.append(factors)
    return tuple(result)


if __name__ == '__main__':
    t = time()
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

    logging.debug("Default speed: {:0.5f} s".format(time() - t))

    t2 = time()

    with multiprocessing.Pool(processes=4) as pool:
        pool.map(factorize, (128, 255, 99999, 10651060))
        logging.debug("Pool speed: {:0.5f} s (used 4 CPUs)".format(time() - t2))

    cpuCount = os.cpu_count()
    print("Number of CPUs in the system:", cpuCount)