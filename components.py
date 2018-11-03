import configparser


def readConfigFile():
    config = configparser.ConfigParser()
    config.read('./serverConfig.conf')
    return config
