import time
from NanoIotController import ControlNano

nano_test = ControlNano('test', 'http://192.168.56.1:8000/')

nano_test.controls()

