#!/usr/bin/env python3

import sys

class DHCalculator:
    inch = 2.54
    pi = 3.14159265359
    joint = {
        -1: { # This is a fake joint (-1) "screwed" to the world's origin (0,0,0)
            "x":0, "y":0, "z":0, "a":0, "b":0, "g":0
        }
    }

    def __init__(self, filename):
        with open(filename) as f:
            i = 0
            for line in f:
                if i > 0:
                    arr = line.strip().split(",")
                    j, x, y, z, a, b, g = list(map(lambda x : float(x), arr))
                    self.joint[int(j)] = {"x":x, "y":y, "z":z, "a":a, "b":b, "g":g}
                i += 1

    def inches_to_meters(self, value):
        return (value / self.inch) * 100

    def deg_to_rad(self, value):
        return value * (self.pi / 180)

    def dh_value_A(self, j):
        j = int(j)
        x_diff = self.joint[j]["x"] - self.joint[j-1]["x"]
        x_diff_meters = self.inches_to_meters(x_diff)
        return round(x_diff_meters, 2)

    def dh_value_ALPHA(self, j):
        rad = self.deg_to_rad(self.joint[j]["a"])
        return round(rad, 9)

    def dh_value_D(self, j):
        j = int(j)
        z_diff = self.joint[j]["z"] - self.joint[j-1]["z"]
        z_diff_meters = self.inches_to_meters(z_diff)
        return round(z_diff_meters, 2)

    def generateHAL(self):
        for j,v in self.joint.items():
            if(j < 0):
                continue
            print("# Joint {j}".format(j=j))
            print("setp genserkins.A-{joint} {dh_A}".format(joint=j, dh_A=self.dh_value_A(j)))
            print("setp genserkins.ALPHA-{joint} {dh_ALPHA}".format(joint=j, dh_ALPHA=self.dh_value_ALPHA(j)))
            print("setp genserkins.D-{joint} {dh_D}".format(joint=j, dh_D=self.dh_value_D(j)))
            print("")


if len(sys.argv) != 2:
    print("Usage: convert.py <file.csv>")
    exit(1)

geometry = DHCalculator(sys.argv[1])
geometry.generateHAL()


