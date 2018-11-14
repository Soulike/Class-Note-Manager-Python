import configparser


# 读取目录下的配置文件
def readConfigFile():
    config = configparser.ConfigParser()
    config.read('./serverConfig.conf')
    return config
