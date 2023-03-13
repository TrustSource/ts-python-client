import abc
import json

from pathlib import Path
from typing import List, Optional, Callable

from . import Command

class Scan(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplemented()


class ScanCommand(Command):
    #Impl = Callable[[List[Path], ...], Optional[Scan]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__impl = None

    def impl(self, impl) -> 'ScanCommand':
        self.__impl = impl
        return self

    def run(self, paths: List[Path], output_path: Optional[Path] = None, *args, **kwargs):
        if self.__impl and (scan := self.__impl(paths, *args, **kwargs)):
            data = scan.to_dict()

            #data['project'] = ''

            if output_path:
                with output_path.open('w') as fp:
                    json.dump(data, fp, indent=2)
            else:
                print(json.dumps(data, indent=2))