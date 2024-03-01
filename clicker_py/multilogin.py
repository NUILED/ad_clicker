import json
import time

from selenium import webdriver
import requests
import itertools


def run_profile(mla_profile_id):
    # mla_profile_id = create_profile()

    mla_url = 'http://127.0.0.1:35000/api/v1/profile/start?automation=true&profileId=' + mla_profile_id

    resp = requests.get(mla_url)

    j = json.loads(resp.content)

    print(resp)
    print(j)

    # Instantiate the Remote Web Driver to connect to the browser profile launched by previous GET request

    driver = webdriver.Remote(command_executor=j['value'])

    return driver


def create_profile():
    x = {
        "name": "testProfile",
        "browser": "mimic",
        "os": "win",
    }
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    url = "http://localhost:35000/api/v2/profile"
    req = requests.post(url, data=json.dumps(x), headers=header)

    return json.loads(req.content).get("uuid")


def delete_profile(mla_profile_id):
    url = "http://localhost:35000/api/v2/profile/" + mla_profile_id
    resp = requests.delete(url)
    print(resp)
    print("profile " + mla_profile_id + " is deleted successfully")


def delete_profile_by_name(profile_name):
    profile_list = list_profiles()
    for i in profile_list:
        if i['name'] == profile_name:
            delete_profile(i['uuid'])


def list_profiles():
    url = "http://localhost:35000/api/v2/profile"
    resp = requests.get(url)
    resp_json = json.loads(resp.content)
    return resp_json


def get_profile_ids():
    profile_list = list_profiles()
    profile_ids = []
    for i in profile_list:
        profile_ids.append(i['uuid'])
    return profile_ids


def delete_all_profiles():
    for i in (get_profile_ids()):
        delete_profile(i)
    print("\nDone deleting all profiles")


def bulk_create(amount_of_profiles):
    for _ in itertools.repeat(None, amount_of_profiles):
        create_profile()
    print(amount_of_profiles.__str__() + " profiles created")


def get_proxies():
    file_path = "ENTER_THE_FILE_PATH_HERE"  # you will need to enter your own proxy details inside the example file
    with open(file_path) as file:
        proxies = json.load(file)
        return proxies


def update_profile_proxy(profile_id, proxy):
    url = 'http://localhost:35000/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "network": {
            "proxy": {
                "type": proxy['type'],
                "host": proxy['host'],
                "port": proxy['port'],
                "username": proxy['username'],
                "password": proxy['password']
            }
        }

    }
    r = requests.post(url, json.dumps(data), headers=header)
    print(r.status_code)


def update_profile_group(profile_id, group_id):
    url = 'http://localhost:35000/api/v2/profile/' + profile_id
    header = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "group": group_id
    }
    r = requests.post(url, json.dumps(data), headers=header)
    print(r.status_code)


def move_profiles_to_group(group_id):
    profile_ids = get_profile_ids()
    for i in profile_ids:
        update_profile_group(i, group_id)


def change_proxies():
    profile_ids = get_profile_ids()
    proxies = get_proxies()
    amount_of_proxies = len(proxies['proxies']['proxy'])
    for i in range(amount_of_proxies):
        update_profile_proxy(profile_ids[i], proxies['proxies']['proxy'][i])
    print('The proxies have been assigned')


def import_cookies(profile_id):
    url = 'http://localhost.multiloginapp.com:35000/api/v1/profile/cookies/import/webext?profileId=' + profile_id
    header = {
        "accept": "*/*",
        "Content-Type": "text/plain"
    }
    file_path = 'ENTER_THE_FILE_PATH_HERE'  # the file should contain cookies in JSON format
    with open(file_path) as file:
        cookies = json.load(file)
        resp = requests.post(url, data=json.dumps(cookies), headers=header)
        print(resp.content)
        print('cookie import finished')


def automation():
    profile_ids = get_profile_ids()
    driver = run_profile(profile_ids[0])
    driver.get('https://app.multiloginapp.com/WhatIsMyIP')
    ip = driver.find_element_by_css_selector('body > div > div.row > div.col-sm-6 > div > '
                                             'div.pti-header.bgm-green > h2')

    region = driver.find_element_by_css_selector('body > div > div.row > div.col-sm-6 > div > '
                                                 'div.pti-header.bgm-green > div')

    print('The IP is ' + ip.text + ' and the region is ' + region.text)
    time.sleep(3)
    driver.quit()


