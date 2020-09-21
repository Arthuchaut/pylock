from pathlib import Path
from pylock.pylock import Pylock
import click

class Main:
    _DEFAULT_REQUIREMENTS: Path = Path('./requirements.txt')
    _DEFAULT_LOCK: Path = Path('./requirements.lock')

    def run() -> None:
        @click.command()
        @click.option(
            '-r', 
            '--requirements', 
            required=True, 
            default=Main._DEFAULT_REQUIREMENTS, 
            help='The requirements file. Default to "./requirements.txt".', 
            type=Path)
        @click.option(
            '-l', 
            '--lock', 
            default=Main._DEFAULT_LOCK, 
            help='The locked file which will be generated. Default to "./requirements.lock".', 
            type=Path)
        def lock(requirements: Path, lock: Path) -> None:
            req_content: List[str] = Pylock.retr_req_pkg(requirements)
            freeze: Dict[str, str] = Pylock.retr_freeze()
            req_freeze: Dict[str, str] = Pylock.filter_pkg(req_content, freeze)
            Pylock.lock_req(req_freeze, lock)

        lock()
        