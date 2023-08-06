import time
import os
import simple_pickle as sp


def log_error(log_data):
    basedir = os.path.abspath(os.path.dirname(__file__)) + "/log/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    now = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime(time.time()))
    if not os.path.exists(basedir + now[:10]):
        sp.write_data('', basedir + now[:10])
    print(now + '  error message    ' + log_data)
    sp.append_data(now + '  error message   ' + log_data + '\n', basedir + now[:10])


def log_info(log_data):
    basedir = os.path.abspath(os.path.dirname(__file__)) + "/log/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
    now = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime(time.time()))
    if not os.path.exists(basedir + now[:10]):
        sp.write_data('', basedir + now[:10])
    print(now + '  info message    ' + log_data)
    sp.append_data(now + '  info message    ' + log_data + '\n', basedir + now[:10])
