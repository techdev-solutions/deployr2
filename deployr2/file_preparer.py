__author__ = 'moritz'
import os
import shutil
import logging


class FilePreparer:
    def __init__(self, deployment_name):
        self.base_path = '/Volumes/Volume/deployr2/' + deployment_name
        self.logger = logging.getLogger(__name__)

    def create_directory_structure(self):
        os.makedirs(self.base_path)
        os.makedirs(self.base_path + '/frontend')
        os.makedirs(self.base_path + '/backend')

    def download_frontend_artifact(self, stream, filename):
        self.__download_artifact(stream, 'frontend', filename)
        # TODO this shouldn't be here...
        # extracting the tar.gz file because we don't want to do that in the docker container
        import tarfile
        tar = tarfile.open(name=self.base_path + '/frontend/' + filename)
        tar.extractall(path=self.base_path + '/frontend/www/')

    def download_backend_artifact(self, stream, filename):
        self.__download_artifact(stream, 'backend', filename)

    def __download_artifact(self, stream, folder, filename):
        self.logger.info('Downloading artifact %s', filename)
        with open(self.base_path + '/' + folder + '/' + filename, 'wb') as f:
            shutil.copyfileobj(stream, f)