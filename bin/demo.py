# -*- coding:utf-8 -*-

import os, sys
basepath = os.path.abspath(os.path.join(os.path.realpath(__file__),'..\..'))
sys.path.append(basepath)

from mod.tools.match import Match
from mod.tools.check import Check

d = [1,2,3]
b = [4,5,6]


print(b+d)