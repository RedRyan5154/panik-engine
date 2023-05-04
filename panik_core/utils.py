import pygame
import time as tm
import random


def random_int(min, max):
    return random.randint(min, max)


class Vec2(pygame.math.Vector2):
    def __init__(self):
        super().__init__()


class Vec3(pygame.math.Vector3):
    def __init__(self):
        super().__init__()


class Timer:
    def __init__(self, delay):
        self.start_time = tm.time()
        self.delay = delay

    def time(self):
        self.end_time = tm.time()
        return self.end_time - self.start_time > self.delay

    def reset(self):
        self.start_time = tm.time()


def sleep(secs):
    tm.sleep(secs)
