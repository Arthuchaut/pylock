from typing import Dict, List, Tuple
import sys
import subprocess
from contextlib import suppress
from pathlib import Path
import re

class Pylock:
    _PYTHON_EXE: str = sys.executable
    _ENCODING: str = 'utf-8'

    def lock_req(req_freeze: Dict[str, str], lock_path: Path) -> None:
        parsed_pkg: str = ''

        for pkg, version in req_freeze.items():
            if re.match(r'git+', pkg):
                parsed_pkg += f'{pkg}'
                continue
                
            parsed_pkg += f'{pkg}=={version}\n'

        with lock_path.open('w') as fh:
            fh.write(parsed_pkg)

    def filter_pkg(req: List[str], freeze: Dict[str, str]) -> Dict[str, str]:
        req_freeze: Dict[str, str] = {}

        for pkg in req:
            if re.match(r'git+', pkg):
                req_freeze[pkg] = ''
                continue

            deps: List[str] = Pylock._retr_pkg_deps(pkg)
            req_freeze[pkg.lower()] = freeze[pkg.lower()]

            for dep in deps:
                req_freeze[dep.lower()] = freeze[dep.lower()]

        return req_freeze

    def retr_req_pkg(req_file: Path) -> List[str]:
        try:
            req_content: str = Path(req_file).read_text(encoding=Pylock._ENCODING)
        except IndexError:
            raise PylockFileError('Requirements file missing from arguments.')
        except FileNotFoundError:
            raise PylockFileError(f'Requirements "{req_file}" not found.')

        return req_content.split('\n')


    def retr_freeze() -> Dict[str, str]:
        freeze: Dict[str, str] = {}
        stdout, stderr = Pylock._syscall([Pylock._PYTHON_EXE, '-m', 'pip', 'freeze'])

        if stderr:
            raise PylockFreezeError(stderr)

        for versionned in stdout.split('\r\n'):
            with suppress(ValueError):
                pkg, version = tuple(versionned.split('=='))
                freeze[pkg.lower()] = version

        return freeze

    def _retr_pkg_deps(pkg: str) -> List[str]:
        stdout, stderr = Pylock._syscall([Pylock._PYTHON_EXE, '-m', 'pip', 'show', pkg])

        # Could be raised by an encoding error, but I'm not resolve this issue yet...
        if stderr:
            raise PylockPackageError(stderr)

        requires: List[str] = [_ for _ in re.search(r'Requires: (.)+', stdout) \
            .group()[10:-1] \
            .split(', ') \
            if _]

        return requires

    def _syscall(cmd: List[str]) -> Tuple[str, str]:
        process: subprocess.Popen = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)

        return (process.communicate()[0].decode(Pylock._ENCODING), 
            process.communicate()[1].decode(Pylock._ENCODING))

class PylockFreezeError(Exception):
    pass

class PylockFileError(Exception):
    pass

class PylockPackageError(Exception):
    pass