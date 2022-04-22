import APIs
from APIs import get_device_list
from APIs import run_http_request

from helpers import write_to_file
from helpers import logger


def check_if_device_is_connected_to_the_internet():
    # Get list of Devices using from SeeTest Cloud
    device_info = get_device_list()

    # Creating empty lists to be populated based on devices Status
    rows_offline = []
    rows_online = []
    rows_in_use = []
    rows_error = []
    rows_unauthorized = []
    rows_not_sure = []

    # Check for each device retrieved
    for i in range(len(device_info)):
        device_property = device_info[i].split('|')
        # Separating out the details: device_id, device_status, device_name, device_udid
        device_properties = device_property[0] + ' | ' + device_property[1] + ' | ' + device_property[2] + ' | ' + device_property[3]

        # Check if device is Offline
        if 'Offline' in device_info[i]:
            logger('Device Offline: ' + device_properties)
            rows_offline.append(device_properties)
        # Check if device is Online
        elif 'Available' in device_info[i]:
            logger('Device Online: ' + device_properties)
            rows_online.append(device_properties)
            rows_online.append(run_http_request(device_property[0], 'https://www.chase.com'))
            rows_online.append("================================================")
        # Check if device is In Use
        elif 'In Use' in device_info[i]:
            logger('Device In Use: ' + device_properties)
            rows_in_use.append(device_properties)
            # rows_online.append(run_http_request(device_property[0], 'https://www.chase.com'))
            # rows_online.append("================================================")
        # Check if device is in Error
        elif 'Error' in device_info[i]:
            logger('Device Error: ' + device_properties)
            rows_error.append(device_properties)
        # Check if device is in Error
        elif 'Unauthorized' in device_info[i]:
            logger('Device Unauthorized: ' + device_properties)
            rows_unauthorized.append(device_properties)
        # Every other Status not captured
        else:
            logger('Not Sure: ' + device_properties)
            rows_not_sure.append(device_properties)

    write_to_file('offline_devices.txt', rows_offline)
    write_to_file('online_devices.txt', rows_online)
    write_to_file('in_use_devices.txt', rows_in_use)
    write_to_file('error_devices.txt', rows_error)
    write_to_file('unauthorized_devices.txt', rows_unauthorized)
    write_to_file('not_sure.txt', rows_not_sure)


if __name__ == '__main__':
    check_if_device_is_connected_to_the_internet()
    # print(APIs.add_device_tag('2025017', 'rahee_test_1'))
    # print(APIs.add_device_tag('2025017', 'rahee_test_2'))
    # print(APIs.add_device_tag('2025017', 'rahee_test_3'))
    # print(APIs.get_device_tags('2025017'))
    # print(run_http_request('2025017', 'https://www.chase.com'))

