import os.path

import helpers
from APIs import get_device_list
from APIs import run_http_request

from helpers import write_to_file
from helpers import create_folder
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
            rows_online.append(run_http_request(device_property[0]))
            rows_online.append("================================================")
        # Check if device is In Use
        elif 'In Use' in device_info[i]:
            logger('Device In Use: ' + device_properties)
            rows_in_use.append(device_properties)
            # rows_online.append(run_http_request(device_property[0]))
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

    folder_path = create_folder()
    write_to_file(folder_path, 'offline_devices', rows_offline)
    write_to_file(folder_path, 'online_devices', rows_online)
    write_to_file(folder_path, 'in_use_devices', rows_in_use)
    write_to_file(folder_path, 'error_devices', rows_error)
    write_to_file(folder_path, 'unauthorized_devices', rows_unauthorized)
    write_to_file(folder_path, 'not_sure', rows_not_sure)


if __name__ == '__main__':
    check_if_device_is_connected_to_the_internet()

