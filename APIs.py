import requests
import json
import configparser
import helpers

from helpers import logger

config = configparser.ConfigParser()
config.read('config.properties')

access_key = helpers.get_access_key()
cloud_url_and_end_point = helpers.get_cloud_url_and_devices_end_point()
url_to_hit = helpers.url_to_hit_for_connectivity_status()


def get_device_list():

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_key
    }

    response = requests.request('GET',
                                cloud_url_and_end_point,
                                headers=headers,
                                verify=False,
                                timeout=60)

    combined_list = []

    if response.status_code == 200:
        logger(
            'Python Script (function: get_device_list) - Successfully retrieved device list from SeeTest Cloud, '
            'response output: %s' % response.text)

        device_id = get_json_values_from_response_content('id', response.content)
        device_status = get_json_values_from_response_content('displayStatus', response.content)
        device_name = get_json_values_from_response_content('deviceName', response.content)
        device_udid = get_json_values_from_response_content('udid', response.content)

        for i in range(len(device_status)):
            combined_list.append(
                str(device_id[i]) + ' | ' + device_status[i] + ' | ' + device_name[i] + ' | ' + device_udid[i])

    else:
        logger(
            'Python Script (function: get_device_list) - Unable to retrieve device list from SeeTest Cloud, '
            'response output: %s' % response.text)

    return combined_list


def run_http_request(device_id):

    # Get a list of current tags from device
    current_tags = get_device_tags(device_id)

    # Checks if device has any existing tags. If tags exists, remove all tags, else skip the step
    if len(current_tags) > 0:
        # Remove Device Tag to begin with as we don't know the state of the device.
        remove_all_device_tags(device_id)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_key
    }

    payload = json.dumps(
        {
            'url': '%s' % url_to_hit
        }
    )

    response = requests.request('POST',
                                cloud_url_and_end_point + '/%s/http-request' % device_id,
                                data=payload,
                                headers=headers,
                                verify=False,
                                timeout=60)

    response_list = []

    try:
        # Retrieve the URL and Status Code as part of the API request
        url = get_singular_json_value_from_response_content('url', response.content)
        status_code = get_singular_json_value_from_response_content('statusCode', response.content)

        # Check if URL is empty, that means the device is in a problematic state, appropriate
        # message will be printed
        if url == '':
            status = get_singular_json_value_from_response_content_from_error('status', response.content)

            # Check if the status is successful, it means that the device is online, but it still couldn't
            # run the http request, this will capture the Error message
            if 'SUCCESS' in status:
                error = get_singular_json_value_from_response_content('error', response.content)

                # If the string Internet is printed as part of the error message
                # it means device does not have internet connection
                if 'internet' in error:
                    remove_all_device_tags(device_id)
                    add_device_tag(device_id, "No_Internet")
                elif 'Internet' in error:
                    remove_all_device_tags(device_id)
                    add_device_tag(device_id, "No_Internet")
                elif 'NSURLErrorDomain' in error:
                    remove_all_device_tags(device_id)
                    add_device_tag(device_id, "No_Internet")
                # elif 'SocketTimeoutException' in error:
                #     remove_all_device_tags(device_id)
                #     add_device_tag(device_id, "Socket_Timeout")

                response_list = ['Error Message: ' + error]
            # If the device is not in SUCCESS state, it means the device is in ERROR, in such case, capture
            # appropriate output
            else:
                message = get_singular_json_value_from_response_content_from_error('message', response.content)
                code = get_singular_json_value_from_response_content_from_error('code', response.content)

                # If Cyder is not in a working state, it means the device is problematic
                # and might need to ge re-connected / rebooted
                # if 'paltielX' in message:
                #     remove_all_device_tags(device_id)
                #     add_device_tag(device_id, "Cyder_Not_Alive")
                # Socket Timeout means device cannot be opened, reboot / re-connect device
                # elif 'SocketTimeoutException' in message:
                #     remove_all_device_tags(device_id)
                #     add_device_tag(device_id, "Socket_Timeout")

                response_list = ['Status: ' + status, 'Message: ' + message, 'Code: ' + code]
        else:
            response_list = ['URL: ' + url, 'Status Code: ' + str(status_code)]
    except:
        print('not sure')

    return response_list


def get_device_tags(device_id):

    headers = {
        'Authorization': 'Bearer %s' % access_key
    }

    response = requests.request('GET',
                                cloud_url_and_end_point + '/%s/tags' % device_id,
                                headers=headers,
                                verify=False)

    if response.status_code == 200:
        logger(
            'Python Script (function: get_device_tags) - Successfully retrieved all tags from device, '
            'response output: %s' % response.text)
        return get_data(response.content)
    else:
        logger(
            'Python Script (function: get_device_tags) - Unable to retrieve tags from device, '
            'response output: %s' % response.text)


def remove_all_device_tags(device_id):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_key
    }

    response = requests.request('DELETE',
                                cloud_url_and_end_point + '/' + device_id + '/tags',
                                headers=headers,
                                verify=False)

    if response.status_code == 200:
        logger(
            'Python Script (function: remove_all_device_tags) - Successfully removed all device tags from device, '
            'response output: %s' % response.text)
    else:
        logger(
            'Python Script (function: remove_all_device_tags) - Unable to remove device tags from device, '
            'response output: %s' % response.text)

    return response


def add_device_tag(device_id, tag_value):

    headers = {
        'Authorization': 'Bearer %s' % access_key,
        'Content-Type': 'application/json'
    }

    response = requests.request('PUT',
                                cloud_url_and_end_point + '/' + device_id + '/tags/' + tag_value,
                                headers=headers,
                                verify=False)

    if response.status_code == 200:
        logger(
            'Python Script (function: add_device_tag) - Successfully added device tag to device, response output: %s' % response.text)
        logger('Python Script (function: add_device_tag) - Device Tag Added: %s' % tag_value)
    else:
        logger(
            'Python Script (function: add_device_tag) - Unable to add device tag to device, response output: %s' % response.text)

    return response


def get_json_values_from_response_content(value, response_content):
    response_list = []
    try:
        data = json.loads(response_content)
        for i in range(len(data['data'])):
            response_list.append(data['data'][i]['%s' % value])
    except Exception as e:
        print(e)
    return response_list


def get_singular_json_value_from_response_content(value, response_content):
    return_value = ''
    try:
        data = json.loads(response_content)
        return_value = data['data']['%s' % value]
    except Exception as e:
        print(e)
    return return_value


# When run_http_request response returns Error, the return output structure is slightly different
# and does not contain "data" in the body.
# For that reason, created this function to get response data with output that does not have "data" in body.
# status / message / code
def get_singular_json_value_from_response_content_from_error(value, response_content):
    return_value = ''
    try:
        data = json.loads(response_content)
        return_value = data['%s' % value]
    except Exception as e:
        print(e)
    return return_value


# Simply returns data content
def get_data(response_content):
    data = json.loads(response_content)
    tags = data['data']
    return tags
