#coding=utf-8
import sys
import configYML
import configINI

logType = None
def initProp(path="python.ini"):
    """
    初始化读取配置
    :return:
    """
    global logType
    if path.endswith(".ini"):
        logType = LogType.INI
        configINI.initProp(path)
    elif path.endswith("yml"):
        logType = LogType.YML
        configYML.initProps(path)
    else:
        print("only support .ini & .yml log format")
        sys.exit(1)


def getPropertyValue(*propName):
    """
    获取配置的值
    :param propName: ini格式的log，只能传单个key； yml格式的log，获取a.b.c的值，可以传a, b, c
    :return:
    """
    global logType
    if logType == LogType.INI:
        return configINI.getPropertyValue(propName[0])
    elif logType == LogType.YML:
        return configYML.getProperty(*propName)
    return None


def setPropertyValue(value, *propName):
    """
    设置配置值
    :param value: key的值
    :param propName: ini格式的log，只能传单个key； yml格式的log，获取a.b.c的值，可以传a, b, c
    :return:
    """
    global logType
    if propName is not None and value is not None:
        if logType == LogType.INI:
            return configINI.setPropertyValue(propName[0], value)
        elif logType == LogType.YML:
            return configYML.setProperty(value, *propName)
    return 0

class LogType():
    YML = "1"
    INI = "2"

