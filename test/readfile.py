import os,sys
basepath = os.path.abspath(os.path.join(os.getcwd(),'..'))
sys.path.append(basepath)

from mod.tools import Check

Check.read_input_args()