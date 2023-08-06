# encoding: utf-8
from cdnutil import basepy
import yaml

props = {}

def initProps(configFile = "python.yml"):
    """
    读取yaml格式配置文件
    :param configFile: 可选，默认读取名称为config.yml
    :return:
    """
    # 获取当前文件的RealPath
    # fileNamePath = os.path.split(os.path.realpath(__file__))[0]

    # 获取配置文件的路径
    # yamlPath = os.path.join(fileNamePath, 'config.yml')

    global props

    # 先读取文件数据，再通过load方法转成字典
    with open(configFile, 'r') as f:
        props = yaml.load(f, Loader=yaml.FullLoader)

    from cdnutil.Log import Logger
    logger = Logger(__name__).getLogger()
    # 不能引用，AttributeError: partially initialized module 'config' has no attribute 'getPropertyValue' (most likely due to a circular import)
    logger.info(props)


def getProperty(*args):
    """
    根据key获取value
    :param args: 可以直接传key，如果key名全局不唯一，也可以传路径，如a.b.key时，args = a, b, key
    :return:
    """
    global props
    if args is None:
        return None

    try:
        tmp = props[args[0]]

        # 根据参数个数，递归获取key对应的值
        for x in range(1, len(args)):
            tmp = tmp[args[x]]
        return tmp
    # KeyError: 'aaa'，抛出异常
    except:
        return None


def setProperty(value=None, *args):
    """
    设置属性
    :param value: 传值，int float str tunple dict
    :param args: 如果属性深度较大，传多个属性即可
    :return:
    """
    global props

    for x in range(len(args)-1, -1, -1) :
        tmp = {}
        tmp[args[x]] = value
        value = tmp

    props.update(value)
    return value

