import json
from typing import List

class Scan(object):
    def __init__(self, module: str, moduleId: str = '', ns: str = ''):
        self.module = module
        self.moduleId = moduleId if moduleId else '{}:{}'.format(ns, module)

        self.type = ''
        self.project = ''
        self.dependencies = []

    @property
    def json(self) -> str:
        return json.dumps(self,
                          default=lambda obj: dict((k, v) for k, v in obj.__dict__.items() if v),
                          indent=2)


class License(object):
    def __init__(self, name: str, url: str = ''):
        self.name = name
        self.url = url


class Dependency(object):
    def __init__(self, key: str, name: str, versions: List[str] = None, licenses: List[License] = None):
        self.key = key
        self.name = name
        self.versions = versions if versions else []
        self.licenses = licenses if licenses else []
        self.dependencies = []

        self.repoUrl = ''
        self.homepageUrl = ''
        self.description = ''

        self.private = False
        self.checksum = ''

        # Meta information
        self.meta = {}


