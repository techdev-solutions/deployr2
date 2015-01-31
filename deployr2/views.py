from django.shortcuts import render
from django.http import HttpResponse
import teamcity


def index(request):
    return render(request, 'deployr2/index.html', {})


def start_deployment_get(request, error=None):
    backend_branches = teamcity.get_branches('Techdev_TrackrBackend')
    frontend_branches = teamcity.get_branches('Techdev_TrackrFrontend')
    model = {
        'backend_branches': backend_branches.json()['branch'],
        'frontend_branches': frontend_branches.json()['branch'],
        'error': error
    }
    return render(request, 'deployr2/start_deployment.html', model)


def start_deployment_post(request):
    try:
        backend_branch = request.POST['backend_branch']
        frontend_branch = request.POST['frontend_branch']
        backend_build_nr = request.POST['backend_build_nr']
        frontend_build_nr = request.POST['frontend_build_nr']
    except KeyError, e:
        return start_deployment_get(request, error=e.message)

    # create random folder
    # download artifacts from teamcity into folder
    # prepare files, like nginx conf and index.html <base tag>
    # create docker container
    # run docker container and mount the created directories
    # save entity into database
    # redirect to entity page

    # TODO this is just temporary...
    return start_deployment_get(request)


def start_deployment(request):
    if request.method == 'GET':
        return start_deployment_get(request)
    elif request.method == 'POST':
        return start_deployment_post(request)


def get_builds_for_build_type_and_branch(request):
    # TODO required parameters!
    branch = request.GET.get('branch')
    build_id = request.GET.get('build_id')
    builds = teamcity.get_builds(build_id, branch)
    return HttpResponse(builds, content_type="application/json")