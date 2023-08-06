#!/usr/bin/env python
# coding=utf-8
import traceback
import getpass
from datetime import datetime

_first_letter = {
    "b": "b", "c": "c", "d": "d", "f": "f", "g": "g", "h": "h", "i": "ch", "j": "j", "k": "k", "l": "l",
    "m": "m", "n": "n", "p": "p", "q": "q", "r": "r", "s": "s", "t": "t", "u": "sh", "v": "zh", "w": "w",
    "x": "x", "y": "y", "z": "z"
}
_second_letter = {
    "a": "a", "b": "in", "c": "ao", "d": "ai", "e": "e", "f": "en", "g": "eng", "h": "ang",
    "i": "i", "j": "an", "k": ["ing", "uai"], "l": ["iang", "uang"], "m": "ian", "n": "iao",
    "o": ["o", "uo"], "p": "ie", "q": "iu", "r": "uan", "s": ["iong", "ong"], "t": ["ue", "ve"],
    "u": "u", "v": ["ui", "v"], "w": "ei", "x": ["ia", "ua"], "y": "un", "z": "ou"
}
_other_letter = {
    "aa": "a", "ah": "ang", "ai": "ai", "an": "an", "ao": "ao", "ee": "e",
    "eg": "eng", "ei": "ei", "en": "en", "er": "er", "oo": "o", "ou": "ou"
}
_valid_words = [
    "jia", "qia", "xia", "gua", "kua", "hua", "zhua", "chua", "shua", "guai", "kuai", "huai",
    "zhuai", "chuai", "shuai", "bing", "ping", "ming", "ding", "ting", "ning", "ling", "jing", "qing",
    "xing", "ying", "guang", "kuang", "huang", "zhuang", "chuang", "shuang", "diang", "niang", "liang",
    "jiang", "qiang", "xiang", "bo", "po", "mo", "fo", "lo", "wo", "duo", "tuo", "nuo", "luo", "guo", "kuo",
    "huo", "zhuo", "chuo", "shuo", "ruo", "zuo", "cuo", "suo", "jiong", "qiong", "xiong", "dong", "tong",
    "nong", "long", "gong", "kong", "hong", "zhong", "chong", "rong", "zong", "cong", "song", "yong",
    "jue", "que", "xue", "yue", "nve", "lve", "dui", "tui", "gui", "kui", "hui", "zhui", "chui", "shui", "rui",
    "zui", "cui", "sui", "nv", "lv"
]

__version__ = "1.2.0"


def believe(func=None):
    if callable(func):
        print("函数{0}受到了感化,函数{0}开始信仰帅副了!".format(func.__name__))

        def do_work(*args):
            try:
                _flag = False
                _argc = len(args)
                if func.__code__.co_argcount > _argc + len(func.__defaults__):
                    print("函数{0}开始工作了,但是帅副指出函数缺少了{1}个参数,并阻止了函数{0}的工作".format(
                        func.__name__,
                        func.__code__.co_argcount - _argc - len(func.__defaults__),
                    ))
                    _flag = True
                if func.__code__.co_argcount < _argc:
                    print("函数{0}开始工作了,但是帅副指出函数多传了{1}个参数,并阻止了函数{0}的工作".format(
                        func.__name__,
                        _argc - func.__code__.co_argcount,
                    ))
                    _flag = True
                if _flag:
                    if func.__doc__:
                        print("帅副觉得你不适合写代码,但是他还是贴心的给你找来了函数的文档{0}".format(func.__doc__))
                    else:
                        print("帅副虽然觉得你不适合写代码,但是这个函数的作者居然不写文档,帅副对于这种行为十分愤慨.")
                    return None
                for i in range(_argc):
                    vn = func.__code__.co_varnames[i]
                    if vn in func.__annotations__ and not isinstance(args[i], func.__annotations__[vn]):
                        if not _flag:
                            print("函数{0}开始工作了,但是帅副觉得有点问题:\n".format(func.__name__))
                        _flag = True
                        print(
                            "帅副觉得给\033[36m{0}\033[0m类型的{1}传了个\033[36m{2}\033[0m的类型的值\033[31m{3}\033[0m就很扯;".format(
                                func.__annotations__[vn].__name__,
                                vn,
                                type(args[i]).__name__,
                                args[i],
                            ))
                res = func(*args)
                if _flag:
                    print("\n但是帅副依然不离不弃,在他的关怀下,函数\033[32m{0}\033[0m依然得出了结果!".format(func.__name__))
                else:
                    print("函数{0}沐浴教旨,努力工作,终于有了结果!".format(func.__name__))
                return res
            except Exception as e:
                print('函数{0}犯了"{1}"的低级错误'.format(func.__name__, str(e)))
                print('\033[1;33m帅副十分心痛!\033[0m')
                err_origin = traceback.extract_tb(e.__traceback__)
                if err_origin[1] is not None:
                    print('他一针见血地指出:\n在文件\033[34m"{0}"\033[0m中的第{1}行的\n\033[7;31m"{2}"\033[0m\n处发生了错误'.format(
                        err_origin[1].filename,
                        err_origin[1].lineno,
                        err_origin[1].line,
                    ))
                    print('仁慈的他决定让{0}解决这个bug,将功赎罪.'.format(getpass.getuser()))
                else:
                    print("帅副对于这种不明所以的错误感到十分愤慨.")

        return do_work
    else:
        print('我信仰帅副!')


def say():
    print('我信仰帅副!')


def holidays(start=2000, end=100):
    for i in range(end):
        day = datetime.strptime("{0}1214".format(start + i), "%Y%m%d").date()
        if day.weekday() in [5, 6]:
            yield day


def translate(text, add_blank=True):
    _result = ""
    _i = 0
    _len = len(text)
    while _i < _len:
        if _i == _len - 1:
            _result += text[_i]
            break
        _t = text[_i] + text[_i + 1]
        _blank = ' ' if _i + 2 < _len and text[_i + 2] != ' ' and add_blank else ''
        if _t in _other_letter:
            _result += (_other_letter[_t] + _blank)
            _i += 1
        elif text[_i] in _first_letter and text[_i + 1] in _second_letter:
            if isinstance(_second_letter[text[_i + 1]], list):
                _w1 = _first_letter[text[_i]] + _second_letter[text[_i + 1]][0]
                _w2 = _first_letter[text[_i]] + _second_letter[text[_i + 1]][1]
                if _w1 in _valid_words:
                    _result += (_w1 + _blank)
                elif _w2 in _valid_words:
                    _result += (_w2 + _blank)
            else:
                _result += _first_letter[text[_i]] + _second_letter[text[_i + 1]] + _blank
            _i += 1
        else:
            _result += text[_i]
        _i += 1
    return _result


def get_version():
    return __version__


fjyi = translate

bjbf = get_version

xbyh = believe

uo = say

jxqi = holidays
