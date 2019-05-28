import requests
import json
from my_meetup_api import meet_up_key
import time
from bs4 import BeautifulSoup
import pickle
import re
from haversine import haversine


def get_group_data(endpoint_url, url_params, start_offset=None, max_offset=None, step_offset=None):
    """returns information called from the meetup API
    endpoint_url -> string
    url_params -> dictionary
    max_offset -> integer"""

    results = []
    url = f"https://api.meetup.com{endpoint_url}?key={meet_up_key}"

    try:
        if start_offset == None or max_offset == None or step_offset == None:
            response = requests.get(url, params=url_params)
            results.extend(response.json())
            return results
        else:
            for i in range(start_offset, max_offset+1, step_offset):
                url_params['offset'] = i
                response = requests.get(url, params=url_params)
                results.extend(response.json())
            return results
    except Exception as e:
        return e


def get_event_data(group_ids):
    """returns information called from the meetup API
    group_ids -> list of integers
    """

    results = []
    total = len(group_ids)
    try:
        for i, id_ in enumerate(group_ids):
            response = requests.get(
                f"https://api.meetup.com/2/events?key={meet_up_key}", params={'group_id': id_})
            results.extend(response.json()['results'])
            print("On {} / {}".format(i+1, total))
            time.sleep(1)
        return results
    except Exception as e:
        return e


def get_member_data2(group_ids):
    """returns information called from the meetup API
    member_ids -> list of integers
    """

    results = []
    total = len(group_ids)

    for i, id_ in enumerate(group_ids):
        try:
            response = requests.get(
                f"https://api.meetup.com/2/members?key={meet_up_key}", params={'group_id': id_})
            if response.status_code == 200:
                results.extend(response.json()['results'])
                print("On {} / {}".format(i+1, total))
                time.sleep(1)
            else:
                pass
        except requests.exceptions.ConnectionError:
            response.status_code = "Connection refused"
    print('Done!')
    return results

# function to get past events for each group for a specified time frame


def get_past_event_data(id_, start, stop):
    """returns information called from the meetup events API
    group_ids -> list of integers
    start -> UNIX Epoch datetime in milliseconds
    stop -> UNIX Epoch datetime in milliseconds
    (stop must be greater than start)
    """

    results = []
    # total = len(group_ids)
    try:
        # for i, id_ in enumerate(group_ids):
        response = requests.get(
            f"https://api.meetup.com/2/events?key={meet_up_key}", params={'group_id': id_, 'time': f"{start},{stop}", 'status': 'past'})
        results.extend(response.json()['results'])
        # print("On {} / {}".format(i+1, total))
        time.sleep(1)
        return results

    except Exception as e:
        return e

# function to get the meetup groups and interest for each member


def get_member_profile(member_url):
    """scrape meetup groups and interest for each member using BeautifulSoup"""

    dict_ = {}
    dict_['member_url'] = member_url
    page = requests.get(member_url)
    soup = BeautifulSoup(page.content, 'html')
    groups = soup.findAll('a', {"class": "omnCamp omngj_pswg4 hoverLink"})
    dict_['groups'] = [g.text.replace('\n', "") for g in groups]

    ints_body = soup.find(id="memberTopicList")
    if ints_body == None:
        dict_['interests'] = ['None']
    else:
        interests = ints_body.findAll('a')
        dict_['interests'] = [i.text for i in interests]

    return dict_


# function to clean text in the description column
def clean_text(description):
    """return cleaned text; requires a string"""
    result1 = re.sub('&lt;br/&gt;', '', re.sub('<[^>]+>', '', description))
    final = re.sub('&lt;/p&gt;', '', re.sub('&amp;', "", result1))
    return final

# function to get haversine distances between venue and each NYC subway station


def get_subway_distances(coord, subway_locations):
    """returns a list of distances from venue to each subway station in NYC, sorted from closest to farthest"""
    return sorted([haversine(coord, s, unit='mi') for s in subway_locations])
