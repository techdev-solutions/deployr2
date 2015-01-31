__author__ = 'moritz'

import requests

teamcity_auth = ('deployr2', 'deployr2')
teamcity_rest_base = 'http://192.168.188.20:8111/app/rest'
accept_json_header = {'Accept': 'application/json'}


def get_branches(build_id):
    return requests.get('%s/buildTypes/id:%s/branches' % (teamcity_rest_base, build_id), auth=teamcity_auth, headers=accept_json_header)


def get_builds(build_id, branch):
    return requests.get(u'{0:s}/builds?locator=buildType:{1:s},branch:{2:s}'.format(teamcity_rest_base, build_id, branch), auth=teamcity_auth, headers=accept_json_header)