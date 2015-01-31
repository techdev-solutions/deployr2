from django.shortcuts import render
from django.http import HttpResponse

import requests

# Create your views here.

teamcity_auth = ('deployr2', 'deployr2')
teamcity_rest_base = 'http://192.168.188.20:8111/app/rest'
accept_json_header = {'Accept': 'application/json'}


def index(request):
    return render(request, 'deployr2/index.html', {})


def start_deployment(request):
    backend_branches = requests.get('%s/buildTypes/id:Techdev_TrackrBackend/branches' % teamcity_rest_base, auth=teamcity_auth, headers=accept_json_header)
    frontend_branches = requests.get('%s/buildTypes/id:Techdev_TrackrFrontend/branches' % teamcity_rest_base, auth=teamcity_auth, headers=accept_json_header)

    return render(request, 'deployr2/start_deployment.html', {'backend_branches': backend_branches.json()['branch'], 'frontend_branches': frontend_branches.json()['branch']})


def get_builds_for_build_type_and_branch(request):
    # TODO required parameters!
    branch = request.GET.get('branch')
    build_id = request.GET.get('build_id')
    builds = requests.get(u'{0:s}/builds?locator=buildType:{1:s},branch:{2:s}'.format(teamcity_rest_base, build_id, branch), auth=teamcity_auth, headers=accept_json_header)
    return HttpResponse(builds, content_type="application/json")