import json
import logging
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from file_preparer import FilePreparer
from teamcity import Teamcity
from models import Deployment

teamcity = Teamcity()
logger = logging.getLogger(__name__)


def index(request):
    deployments = Deployment.objects.all()
    return render(request, 'deployr2/index.html', {'deployments': deployments})


def start_deployment_form(request, error=None):
    backend_branches = teamcity.get_branches('Techdev_TrackrBackend')
    frontend_branches = teamcity.get_branches('Techdev_TrackrFrontend')
    model = {
        'backend_branches': backend_branches,
        'frontend_branches': frontend_branches,
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

    from uuid import uuid4
    deployment_name = str(uuid4())
    logger.info('Creating deployment %', deployment_name)

    file_preparer = FilePreparer(deployment_name)
    file_preparer.create_directory_structure()

    backend_artifact = ''
    # download artifacts from teamcity into folder
    for artifact in teamcity.get_artifacts(backend_build_id):
        # TODO hack, the backend artifact name should not be from here!
        if artifact.name.endswith('jar'):
            backend_artifact = artifact.name
        res = teamcity.stream_artifact(artifact.content_link)
        file_preparer.download_backend_artifact(res.raw, artifact.name)

    for artifact in teamcity.get_artifacts(frontend_build_id):
        res = teamcity.stream_artifact(artifact.content_link)
        file_preparer.download_frontend_artifact(res.raw, artifact.name)

    # prepare files index.html <base tag>
    # create docker container
    from docker import Client
    c = Client('unix://var/run/docker.sock')

    backend_container = c.create_container(image='java:openjdk-8', command='java -jar ' + backend_artifact, detach=True, name='backend_' + deployment_name, volumes=['/opt/trackr-backend'],
                                           working_dir='/opt/trackr-backend')
    c.start(backend_container['Id'], binds={'/opt/techdev/deployr2/deployments/%s/backend' % deployment_name: {'bind': '/opt/trackr-backend', 'ro': True}})

    frontend_container = c.create_container(image='nginx', ports=[80], name='frontend_' + deployment_name, volumes=['/etc/nginx/conf.d/default.conf', '/usr/share/nginx/html'])
    c.start(frontend_container['Id'], links=[('backend_' + deployment_name, 'backend')], publish_all_ports=True, binds={
        '/opt/techdev/deployr2/default.conf': {'bind': '/etc/nginx/conf.d/default.conf', 'ro': True},
        '/opt/techdev/deployr2/deployments/%s/frontend/www' % deployment_name: {'bind': '/usr/share/nginx/html', 'ro': True}
    })

    inspect = c.inspect_container('frontend_' + deployment_name)
    frontend_port = inspect['NetworkSettings']['Ports']['80/tcp'][0]['HostPort'] # Help!!!

    # create an entity so we know of this deployment later
    from django.utils import timezone
    deployment = Deployment(id=deployment_name, create_date=timezone.now())
    deployment.save()

    import augeas
    a = augeas.Augeas(root='/')
    a.defvar('host', '/files/etc/apache2/sites-available/deployr.conf')
    a.defnode('newloc', '$host/VirtualHost/Location[last() + 1]', '')
    a.set('$newloc/arg', '/' + deployment_name)
    a.set('$newloc/directive', 'ProxyPass')
    a.set('$newloc/*[self::directive="ProxyPass"]/arg[1]', 'http://localhost:' + frontend_port)
    a.save()

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
    return HttpResponse(json.dumps([build.__dict__ for build in builds]), content_type="application/json")


def get_deployment(request, deployment_name):
    deployment = Deployment.objects.get(id=deployment_name)
    return render(request, 'deployr2/deployment.html', {'deployment': deployment})


def delete_deployment(request, deployment_name):
    deployment = Deployment.objects.get(id=deployment_name)

    # confirm docker containers are stopped
    # remove docker containers inclusive volumes

    # remove folders
    import shutil
    from django.conf import settings
    shutil.rmtree(settings.DEPLOYR2_DEPLOYMENTS + deployment.id)

    # remove entity
    deployment.delete()

    return HttpResponseRedirect(reverse('deployr2:index'))