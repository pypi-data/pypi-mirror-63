from itertools import chain
from random import choice
from pathlib import Path
from datetime import timedelta
from click import progressbar
from ..defines import MURDER_DAY, ACCESS_POINT_OF_INTEREST
from ..people import MAIN_DETECTIVE, SUSPECTS, FACTORY_WORKERS
from ..fillers import random_datetimes
from ..git_utils import git_commit, in_branch

@in_branch(f'detectives/{MAIN_DETECTIVE.username}')
def build_phase_2(repo):
    evidence_dir = Path(repo.working_tree_dir) / 'evidence'
    evidence_dir.mkdir()
    access_log = evidence_dir / 'access.log'

    # We commit each suspect's entry in reverse so that `git log` will lead first to the first
    # suspect's interview on the next step.
    (entry_1, entry_2, entry_3, ) = reversed(SUSPECTS)
    access_points = (
        'DOOR_FRONT_1', 'DOOR_FRONT_2', 'CABINET_34_A', 'CABINET_67_C1', 'MAIN_FREEZER',
        'BACK_ROOM_231', 'SECURITY_ROOM_1', 'SECURITY_ROOM_2', 'PRINTER_ROOM_76',
    )

    chunks = (17, 5, 12, 9)
    logs = zip(
        chain((choice(FACTORY_WORKERS) for _ in range(chunks[0])),
              [entry_1, ],
              (choice(FACTORY_WORKERS) for _ in range(chunks[1])),
              [entry_2, ],
              (choice(FACTORY_WORKERS) for _ in range(chunks[2])),
              [entry_3, ],
              (choice(FACTORY_WORKERS) for _ in range(chunks[3]))),
        chain((choice(access_points) for _ in range(chunks[0])),
              [ACCESS_POINT_OF_INTEREST, ],
              (choice(access_points) for _ in range(chunks[1])),
              [ACCESS_POINT_OF_INTEREST, ],
              (choice(access_points) for _ in range(chunks[2])),
              [ACCESS_POINT_OF_INTEREST, ],
              (choice(access_points) for _ in range(chunks[3]))),
        random_datetimes(sum(chunks), MURDER_DAY, MURDER_DAY + timedelta(days=1), hour_max=18))
    with progressbar(logs, length=sum(chunks) + len(SUSPECTS),
            label='Comitting factory access logs') as bar:
        for (worker, access_point, time) in bar:
            with access_log.open('a') as l:
                l.write(f'{access_point}\n')
            repo.index.add(access_log.as_posix())
            git_commit(repo, worker, time, f'ACCESS LOG COMMIT {time:%H:%M}')
