#coding=utf-8
import configparser
import json

kv = {}

def initProp(path="python.ini"):
    """
    初始化读取配置
    :return:
    """
    global kv

    cf = configparser.ConfigParser()
    filename = cf.read(path, "utf-8")
    # 得到所有section，即[mysql],[server]等
    sections = cf.sections()
    # 得到mysql section所有相关配置
    for section in sections:
        list = cf.items(section)
        for tunlp in list:
            kv[tunlp[0]]=tunlp[1]

    if cf.has_section("parse_list"):
        for section in sections:
            try:
                tmp = cf.get("parse_list", section)
                if tmp is not None:
                    tmp = tmp.replace(" ", "").split(",")
                    for key in tmp:
                        str_list_or_tunple = cf.get("es_base", key)
                        list_or_tunple = json.loads(str_list_or_tunple)
                        kv[key] = list_or_tunple
                        print(str_list_or_tunple + " " + str(type(list_or_tunple)))
            except:
                pass

    from cdnutil.Log import Logger
    logger = Logger(__name__).getLogger()
    # 不能引用，AttributeError: partially initialized module 'config' has no attribute 'getPropertyValue' (most likely due to a circular import)
    logger.info(kv)

    print (kv)


def getPropertyValue(propName):
    """
    获取配置的值
    :param propName:
    :return:
    """
    global kv
    return kv[propName]


def setPropertyValue(propName, value):
    """
    设置配置值
    :param propName:
    :param value:
    :return:
    """
    if propName is not None and value is not None:
        global kv
        kv[propName] = value
        return 1

    return 0

