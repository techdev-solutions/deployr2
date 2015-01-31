from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import teamcity
from models import Deployment


def index(request):
    deployments = Deployment.objects.all()
    return render(request, 'deployr2/index.html', {'deployments': deployments})


def start_deployment_form(request, error=None):
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
        backend_build_id = request.POST['backend_build_id']
        frontend_build_id = request.POST['frontend_build_id']
    except KeyError, e:
        return start_deployment_form(request, error=e.message)

    # create random folder
    from uuid import uuid4
    deployment_name = str(uuid4())

    import os
    # TODO check if deployment already exists
    os.makedirs('/Volumes/Volume/deployr2/%s' % deployment_name)
    os.makedirs('/Volumes/Volume/deployr2/%s/%s' % (deployment_name, 'frontend'))
    os.makedirs('/Volumes/Volume/deployr2/%s/%s' % (deployment_name, 'backend'))

    # download artifacts from teamcity into folder
    # import shutil
    # backend_artifacts = teamcity.get_artifacts(backend_build_id).json()['file']
    # for artifact in backend_artifacts:
    #     res = teamcity.stream_artifact(artifact['content']['href'])
    #     with open('/Volumes/Volume/deployr2/%s/backend/%s' % (deployment_name, artifact['name']), 'wb') as f:
    #         res.raw.decode_content = True
    #         shutil.copyfileobj(res.raw, f)
    #
    # frontend_artifacts = teamcity.get_artifacts(frontend_build_id).json()['file']
    # for artifact in frontend_artifacts:
    #     res = teamcity.stream_artifact(artifact['content']['href'])
    #     with open('/Volumes/Volume/deployr2/%s/frontend/%s' % (deployment_name, artifact['name']), 'wb') as f:
    #         res.raw.decode_content = True
    #         shutil.copyfileobj(res.raw, f)

    # prepare files, like nginx conf and index.html <base tag>
    # create docker container
    # run docker container and mount the created directories

    # create an entity so we know of this deployment later
    from django.utils import timezone
    deployment = Deployment(id=deployment_name, create_date=timezone.now())
    deployment.save()

    return HttpResponseRedirect(reverse('deployr2:deployment', kwargs={'deployment_name': deployment_name}))


def start_deployment(request):
    if request.method == 'GET':
        return start_deployment_form(request)
    elif request.method == 'POST':
        return start_deployment_post(request)


def get_builds_for_build_type_and_branch(request):
    # TODO required parameters!
    branch = request.GET.get('branch')
    build_id = request.GET.get('build_id')
    builds = teamcity.get_builds(build_id, branch)
    return HttpResponse(builds, content_type="application/json")


def get_deployment(request, deployment_name):
    deployment = Deployment.objects.get(id=deployment_name)
    return render(request, 'deployr2/deployment.html', {'deployment': deployment})


def delete_deployment(request, deployment_name):
    deployment = Deployment.objects.get(id=deployment_name)

    # confirm docker containers are stopped
    # remove docker containers inclusive volumes

    # remove folders
    import shutil
    shutil.rmtree('/Volumes/Volume/deployr2/%s' % deployment.id)

    # remove entity
    deployment.delete()

    return HttpResponseRedirect(reverse('deployr2:index'))