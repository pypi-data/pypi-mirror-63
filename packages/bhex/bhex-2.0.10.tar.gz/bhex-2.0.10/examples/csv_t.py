# coding: utf-8
import csv
import threading


class Test(object):

    def __init__(self):
        self.name = 'kobe'

    def test(self):

        def func():
            print(self.name)


        func()


if __name__ == '__main__':
    Test().test()
