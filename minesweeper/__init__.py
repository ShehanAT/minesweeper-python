"""
The init file for the minesweeper package.

Original Author: Yuhuang Hu 
Author email: duguyue100@gmail.com

"""
import os 
from minesweeper.msgame import MSGame 
from minesweeper.msboard import MGBoard 

PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
PACKAGE_IMGS_PATH = os.path.join(PACKAGE_PATH, "imgs")