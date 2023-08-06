from .ihex import parseIHex
from .loader import Loader
from .device import device_list

import progressbar
import serial
import sys
import time
import math

def do_prog(args):

    # flash_data = b''
    # if args.is_prog_flash:
    #     flash_data = parseIHex(args.flash_file)

    # eep_data = b''
    # if args.is_prog_eep:
    #     eep_data = parseIHex(args.eep_file)

    ser = serial.Serial()
    ser.port = args.port
    ser.baudrate = 115200
    ser.timeout = 1
    try:
        ser.open()
    except:
        print("錯誤：串列埠 {0} 已經被占用".format(args.port))
        sys.exit(1)
    
    loader = Loader(ser, args)

    # print('flash  花費大小為 {0:0.2f} KB ({1} bytes) 。'.format(len(flash_data)/1024, len(flash_data)))
    # print('eeprom 花費大小為 {0} bytes。'.format(len(eep_data)))

    # cost_t = math.ceil(len(flash_data)/256) * 0.047 + math.ceil(len(eep_data)/256) * 0.05 + 0.23
    # print('預估花費時間為 {0} s。'.format(cost_t))

    widgets=[
        ' [', progressbar.Timer('Elapsed Time: %(seconds)s s', ), '] ',
        progressbar.Bar(),
        progressbar.Counter(format='%(percentage)0.2f%%'),
    ]
    bar = progressbar.ProgressBar(max_value=loader.total_steps, widgets=widgets)
    bar.update(0)
    for i in range(loader.total_steps):
        try:
            loader.do_step()
            bar.update(i)
        except:
            bar.finish(end='\n', dirty=True)
            raise Exception
