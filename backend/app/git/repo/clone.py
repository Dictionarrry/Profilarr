# git/clone_repo.py

import os
import shutil
import logging
import yaml
from git.exc import GitCommandError
import git
from ..auth.authenticate import validate_git_token

logger = logging.getLogger(__name__)


def clone_repository(repo_url, repo_path):
    try:
        temp_dir = f"{repo_path}_temp"
        backup_dir = f"{repo_path}_backup"

        logger.info(f"Cloning repository from {repo_url} to {temp_dir}")

        try:
            repo = git.Repo.clone_from(repo_url, temp_dir)
            logger.info("Repository cloned successfully")
        except GitCommandError as e:
            if "remote: Repository not found" in str(e):
                logger.info(
                    "Repository not found. Creating a new empty repository.")
                repo = git.Repo.init(temp_dir)
                repo.create_remote('origin', repo_url)
            else:
                logger.error(f"Git clone failed: {str(e)}")
                return False, f"Failed to clone repository: {str(e)}"

        try:
            repo.head.reference
        except ValueError:
            logger.info(
                "Repository is empty. Initializing with basic structure.")
            _initialize_empty_repo(repo)

        if os.path.exists(repo_path):
            logger.info(f"Backing up existing repo to {backup_dir}")
            shutil.move(repo_path, backup_dir)

        logger.info(f"Moving cloned repo from {temp_dir} to {repo_path}")
        shutil.move(temp_dir, repo_path)

        for folder_name in ['regex_patterns', 'custom_formats', 'profiles']:
            folder_path = os.path.join(repo_path, folder_name)
            backup_folder_path = os.path.join(backup_dir, folder_name)

            if not os.path.exists(folder_path):
                logger.info(f"Creating missing folder: {folder_name}")
                os.makedirs(folder_path)

            # Get existing files from cloned repo
            cloned_files = set(
                f.replace('.yml', '') for f in os.listdir(folder_path)
                if f.endswith('.yml'))

            if os.path.exists(backup_folder_path):
                local_files = [
                    f for f in os.listdir(backup_folder_path)
                    if f.endswith('.yml')
                ]

                for file_name in local_files:
                    old_file_path = os.path.join(backup_folder_path, file_name)
                    with open(old_file_path, 'r') as file:
                        data = yaml.safe_load(file)

                    # Use name as the identifier
                    base_name = data['name']
                    new_name = base_name
                    counter = 1

                    # If name exists, append a number
                    while new_name in cloned_files:
                        new_name = f"{base_name} ({counter})"
                        counter += 1

                    cloned_files.add(new_name)

                    new_file_path = os.path.join(folder_path,
                                                 f"{new_name}.yml")
                    with open(new_file_path, 'w') as file:
                        yaml.dump(data, file)
                    logger.info(f"Merged local file: {new_name}.yml")

        if os.path.exists(backup_dir):
            logger.info(f"Removing backup directory: {backup_dir}")
            shutil.rmtree(backup_dir)

        logger.info("Repository cloned and set up successfully")
        return True, "Repository cloned successfully and local files updated"
    except Exception as e:
        logger.exception("Unexpected error during repository cloning")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(backup_dir):
            shutil.move(backup_dir, repo_path)
        return False, f"Unexpected error: {str(e)}"


def _initialize_empty_repo(repo):
    # Create basic folder structure
    os.makedirs(os.path.join(repo.working_tree_dir, 'regex_patterns'),
                exist_ok=True)
    os.makedirs(os.path.join(repo.working_tree_dir, 'custom_formats'),
                exist_ok=True)
    os.makedirs(os.path.join(repo.working_tree_dir, 'quality_profiles'),
                exist_ok=True)

    # Create a README file
    with open(os.path.join(repo.working_tree_dir, 'README.md'), 'w') as f:
        f.write(
            "# Profilarr Repository\n\nThis repository contains regex patterns, custom formats and quality profiles."
        )

    repo.git.add(A=True)
    repo.index.commit("Initial commit: Basic repository structure")
    repo.create_head('main')
    repo.heads.main.checkout()
    origin = repo.remote(name='origin')
    origin.push('main')
    origin.push('main:main')

    logger.info(
        f"Initialized empty repository with basic structure and pushed to main"
    )
