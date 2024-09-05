import abc
import json

from pathlib import Path
from click import Command

from typing import List, Optional

class Scan(abc.ABC):
    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplemented()


class ScanCommand(Command):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__impl = None

    # Impl = Callable[[List[Path], ...], Union[Optional[Scan], Iterable[Scan]]]
    # Type hint not used due to issues with earlier Python versions
    def impl(self, impl) -> 'ScanCommand':
        """
        :param impl: Callable[[List[Path], ...], Union[Optional[Scan], Iterable[Scan]]]
        :return: self
        """
        self.__impl = impl
        return self

    def run(self, paths: List[Path], output_path: Optional[Path] = None, *args, **kwargs):
        if self.__impl and (scan := self.__impl(paths, *args, **kwargs)):
            if isinstance(scan, Scan):
                data = scan.to_dict()
            else:
                data = []
                for s in scan:
                    if not isinstance(s, Scan):
                        raise ValueError('Unexpected scan type')
                    data.append(s.to_dict())

            if output_path:
                output_path = output_path.resolve()
                with output_path.open('w') as fp:
                    json.dump(data, fp, indent=2)
            else:
                print(json.dumps(data, indent=2))