import sys
from PyQt5 import uic
import cv2, imutils
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import datetime
import os
import numpy as np
from PIL import Image
import io
from PyQt5.QtCore import QByteArray, QBuffer

from_class = uic.loadUiType("/home/ryu/amr_ws/opencv/src/opencv_oneday.ui")[0]