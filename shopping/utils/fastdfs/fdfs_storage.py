from django.conf import settings
from django.core.files.storage import Storage

class FdfsStorage(Storage):
    def __init__(self,dfsbaseurl=None):
        self.dfsbaseurl = dfsbaseurl or settings.FASTDFS_BASE_URL
    def _open(self, name, mode='rb'):
        pass
    def _save(self, name, content):
        pass
    def url(self, name):
        return self.dfsbaseurl+name