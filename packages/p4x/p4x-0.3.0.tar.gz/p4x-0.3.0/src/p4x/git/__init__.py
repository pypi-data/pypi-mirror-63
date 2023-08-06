import json
import pathlib as pl
from typing import Union

import git
import git.exc


def export_remote(p: Union[str, pl.Path]):
    try:
        # create a git repo object
        repo = git.Repo(p.resolve())
        remote: git.Remote
        # get all remotes and their URLs
        remotes = dict(
                (remote.name, list(remote.urls)) for remote in repo.remotes)

        # write to file ".gitremotes" as JSON-formatted string
        with (p / '.gitremotes').open('w') as f:
            json.dump(remotes, f, indent=4)
    except git.InvalidGitRepositoryError:
        pass
