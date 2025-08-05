import os
import shutil
import tempfile
from urllib.parse import urlparse, urlunparse
from git import Repo, GitCommandError

def clone_git_repo(git_url: str, username: str = None, password: str = None) -> str:
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    try:
        if username and password:
            parsed_url = urlparse(git_url)
            netloc = f"{username}:{password}@{parsed_url.netloc}"
            auth_url = urlunparse(parsed_url._replace(netloc=netloc))
        else:
            auth_url = git_url
        Repo.clone_from(auth_url, temp_dir)
        return temp_dir
    except GitCommandError as e:
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"Git clone error: {e}")
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise RuntimeError(f"Unexpected error during cloning: {e}")

def scan_repo_structure(path: str):
    repo_files = []
    for root, _, files in os.walk(path):
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), path)
            repo_files.append(rel_path)
    return repo_files
