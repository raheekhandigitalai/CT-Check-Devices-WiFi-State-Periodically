from APIs import get_device_list
from APIs import run_http_request
from APIs import add_device_tag
from APIs import remove_all_device_tags

from helpers import write_to_file
from helpers import logger


def test():
    device_info = get_device_list()

    rows_offline = []
    rows_online = []
    rows_in_use = []
    rows_error = []
    rows_not_sure = []

    for i in range(len(device_info)):
        device_property = device_info[i].split('|')
        device_properties = device_property[0] + ' | ' + device_property[1] + ' | ' + device_property[2] + ' | ' + device_property[3]

        if 'Offline' in device_info[i]:
            logger('Device Offline: ' + device_properties)
            rows_offline.append(device_properties)
        elif 'Available' in device_info[i]:
            logger('Device Online: ' + device_properties)
            rows_online.append(device_properties)
            rows_online.append(run_http_request(device_property[0], 'https://www.chase.com'))
            rows_online.append("================================================")
        elif 'In Use' in device_info[i]:
            logger('Device In Use: ' + device_properties)
            rows_in_use.append(device_properties)
        elif 'Error' in device_info[i]:
            logger('Device Error: ' + device_properties)
            rows_error.append(device_properties)
        else:
            logger('Not Sure: ' + device_properties)
            rows_not_sure.append(device_properties)

    write_to_file('offline_devices.txt', rows_offline)
    write_to_file('online_devices.txt', rows_online)
    write_to_file('in_use_devices.txt', rows_in_use)
    write_to_file('error_devices.txt', rows_error)
    write_to_file('not_sure.txt', rows_not_sure)


if __name__ == '__main__':
    test()

