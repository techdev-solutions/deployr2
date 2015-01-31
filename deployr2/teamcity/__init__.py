__author__ = 'moritz'

import requests

teamcity_auth = ('deployr2', 'deployr2')
teamcity_rest_base = 'http://192.168.188.20:8111/app/rest'
teamcity_base = 'http://192.168.188.20:8111'
accept_json_header = {'Accept': 'application/json'}


# base request for almost all TeamCity accesses
def base_request(path):
    return requests.get('%s/%s' % (teamcity_rest_base, path), auth=teamcity_auth, headers=accept_json_header)


def get_branches(build_type):
    """
    :param build_type: The build type like Techdev_TrackrFrontend
    :return: All active branches for that build type
    """
    return base_request('buildTypes/id:%s/branches' % build_type)


def get_builds(build_type, branch):
    """
    :param build_type: The build type, like Techdev_TrackrFrontend
    :param branch: A branch name
    :return: All builds for the selected type and branch
    """
    return base_request('builds?locator=buildType:%s,branch:%s' % (build_type, branch))


def get_artifacts(build_id):
    """
    :param build_id: The id of the build which is numeric
    :return: A JSON response with all artifacts for that build
    """
    return base_request('builds/id:%s/artifacts' % build_id)


def stream_artifact(path):
    """
    :param path The full URI to the artifact, like /app/rest/builds/id:56/artifacts/content/trackr-backend-1.0-build-16.jar
    :return: The HTTP response as a with a streamable raw body
    """
    return requests.get('%s%s' % (teamcity_base, path), auth=teamcity_auth, stream=True)