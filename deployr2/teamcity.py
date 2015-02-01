__author__ = 'moritz'

import requests


class Teamcity:
    def __init__(self):
        from django.conf import settings
        self.teamcity_auth = (settings.DEPLOYR2_TEAMCITY_USER, settings.DEPLOYR2_TEAMCITY_PASSWORD)
        self.teamcity_base = settings.DEPLOYR2_TEAMCITY_SERVER
        self.teamcity_rest_base = self.teamcity_base + '/app/rest'

    def __base_request(self, path):
        accept_json_header = {'Accept': 'application/json'}
        return requests.get('%s/%s' % (self.teamcity_rest_base, path), auth=self.teamcity_auth, headers=accept_json_header)

    def get_branches(self, build_type):
        """
        :param build_type: The build type like Techdev_TrackrFrontend
        :return: All active branches for that build type
        """
        response = self.__base_request('buildTypes/id:%s/branches' % build_type)
        return [Branch(branch['name']) for branch in response.json()['branch']]

    def get_builds(self, build_type, branch):
        """
        :param build_type: The build type, like Techdev_TrackrFrontend
        :param branch: A branch name
        :return: All builds for the selected type and branch that are not running anymore and were successful.
        """
        response = self.__base_request('builds?locator=buildType:%s,branch:%s,running:false,status:SUCCESS' % (build_type, branch))
        return [Build(build['number'], build['id']) for build in response.json()['build']]

    def get_artifacts(self, build_id):
        """
        :param build_id: The id of the build which is numeric
        :return: A JSON response with all artifacts for that build
        """
        response = self.__base_request('builds/id:%s/artifacts' % build_id)
        return [Artifact(artifact['name'], artifact['content']['href']) for artifact in response.json()['file']]

    def stream_artifact(self, path):
        """
        :param path The full URI to the artifact, like /app/rest/builds/id:56/artifacts/content/trackr-backend-1.0-build-16.jar
        :return: The HTTP response as a with a streamable raw body
        """
        return requests.get('%s%s' % (self.teamcity_base, path), auth=self.teamcity_auth, stream=True)


class Branch:
    def __init__(self, name):
        self.name = name


class Build:
    def __init__(self, number, id):
        self.number = number
        self.id = id


class Artifact:
    def __init__(self, name, content_link):
        self.name = name
        self.content_link = content_link