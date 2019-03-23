# -*- coding:utf-8 -*-

import time, functools

class Debug(object):
    """调试类，显示调试信息"""

    @staticmethod
    def get_time_cost(content):
        """
        装饰器，如果debug模式开启，则显示函数运行的时间
        :param content: 仅仅作为显示，类行为字符串
        """
        from mod.tools.check import Check

        def decorator(func):
            @functools.wraps(func)  # 处理原始函数__name__等属性
            def wrapper(*args, **kwargs):
                if Check.get_debug_level() == 'debug':
                    start_time = time.time()
                    value = func(*args, **kwargs)
                    end_time = time.time()
                    cost_time = round((end_time - start_time), 3)   # round 来控制精度
                    print('{content}耗时 {cost_time} ms'.format(content=content, cost_time=cost_time))
                    return value
                else:
                    return func(*args, **kwargs)

            return wrapper
        return decorator