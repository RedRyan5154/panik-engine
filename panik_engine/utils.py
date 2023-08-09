import pygame
import time as tm
import random, math


start_time = tm.time()


def runtime():
    global start_time
    return float(tm.time() - start_time)


def random_int(min, max):
    return random.randint(min, max)


def random_float(min, max):
    """
    Return a random float with up to 4 decimals"""
    return random.randint(min * 10000, max * 10000) / 10000


class Vec2(pygame.math.Vector2):
    def __init__(self, x=None, y=None):
        super().__init__(x, y)


class Vec3(pygame.math.Vector3):
    def __init__(self, x=None, y=None, z=None):
        super().__init__(x, y, z)


class Timer:
    def __init__(self, delay):
        self.start_time = tm.time()
        self.delay = delay

    def time(self):
        self.end_time = tm.time()
        return self.end_time - self.start_time > self.delay

    def reset(self, delay=None):
        if delay:
            self.delay = delay
        self.start_time = tm.time()


def sleep(secs):
    tm.sleep(secs)


def lerp(a, b, t):
    return (1 - t) * a + t * b


def ilerp(a, b, v):
    return (v - a) / (b - a)


def lerp_angle(a, b, t):
    return a + (((b - a) + 180) % 360 - 180) * t
