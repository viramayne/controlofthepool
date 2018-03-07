#  ­*­ coding: utf­8 ­*­
__author__ = 'vira'

from threading import Timer


class ModelTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction

    def handle_function(self, t):
        self.hFunction()

    def start(self):
        self.thread = Timer(self.t, self.hFunction)
        self.thread.start()

    def cancel(self):
        self.thread.cancel()