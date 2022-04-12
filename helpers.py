import configparser

config = configparser.ConfigParser()
config.read('config.properties')


def write_to_file(file_name, items):
    with open(file_name, 'w') as f:
        for item in items:
            f.write("%s\n" % item)


def logger(message):
    print(message)


def get_access_key():
    return config.get('seetest_authorization', 'access_key')


def get_cloud_url_and_devices_end_point():
    return config.get('seetest_urls', 'cloud_url') + config.get('seetest_urls', 'end_point')