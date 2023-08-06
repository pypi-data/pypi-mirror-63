basepy.py           python2.7环境下用于解决打印乱码问题
                    同时支持python版本查询
cdnmstk.py          用于token的存储和获取（放在一个指定文件中）
common.py           公共类
config.py           用于存储交运运行起来的配置，配置文件支持在
                    启动脚本中指定，如果不指定，默认是python.ini
                    如需使用，应该放在Log.py之前引入并初始化
Log.py              日志打印，走配置