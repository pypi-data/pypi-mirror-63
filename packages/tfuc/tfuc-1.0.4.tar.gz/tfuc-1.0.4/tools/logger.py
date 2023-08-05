from tools.timer import Time
# import traceback
import sys
from threading import Lock


# import inspect

# 获取被调用函数所在模块文件名
# print(inspect.stack()[1][1])
# print(sys._getframe(1).f_code.co_filename)

# 获取被调用函数名称
# print(inspect.stack()[1][3])
# print(sys._getframe(1).f_code.co_name)

# 获取被调用函数在被调用时所处代码行数
# print(inspect.stack()[1][2])
# print(sys._getframe(1).f_lineno)


class Logger(object):
    def __init__(self, level=0):
        self.level = level
        self.fmt = '\r[{}] [{}] [{}]: {}'
        self.mode = ['\033[1;32mINFO\033[0m', '\033[1;33mWARNING\033[0m', '\033[1;31mERROR\033[0m']
        self.time = Time()
        self.time.set_fmt('%H:%M:%S')
        self.pre_module = sys._getframe(1).f_code.co_filename.split('/')[-1].split('.')[0]
        self.lock = Lock()

    def info(self, msg):
        level = 1
        if level >= self.level:
            mode = self.mode[level - 1]
            self.lock.acquire()
            print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, msg))
            self.lock.release()

    def warning(self, msg):
        level = 2
        if level >= self.level:
            mode = self.mode[level - 1]
            self.lock.acquire()
            print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, msg))
            self.lock.release()

    def error(self, msg=None):
        level = 3
        if level >= self.level:
            self.lock.acquire()
            mode = self.mode[level - 1]
            type_, value_, traceback_ = sys.exc_info()
            ex = traceback.format_exception(type_, value_, traceback_)
            print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, '*' * 100))
            for i in ex[1:]:
                print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, i.splitlines(True)[0].strip()))
            if msg:
                print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, msg))
            print(self.fmt.format(self.time.get_fmt_time, self.pre_module, mode, '*' * 100))
            self.lock.release()

    def __call__(self, *args, **kwargs):
        self.info(args, kwargs)
