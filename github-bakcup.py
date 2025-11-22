import argparse
import logging
import os
import shutil
import subprocess
import sys

import requests

logger = logging.getLogger(__name__)

def clone_all_repos(username):
    # remove old dir if exists
    if os.path.exists(username):
        shutil.rmtree(username)

    # create new directory
    if not os.path.exists(username):
        os.makedirs(username)
    
    logger.debug(f"Fetching {username} repositories")
    
    page = 1
    repos_count = 0
    fail_count = 0
    
    while True:
        # fetch public repo list for given user
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
        try:
            response = requests.get(url)
            if response.status_code == 404:
                logger.error("User not found")
                fail_count = 999
                return
            if response.status_code != 200:
                logger.error(f"Error fetching repository list: {response.status_code}")
                fail_count = 999
                return

            repos = response.json()
            
            # all repos found
            if not repos:
                break

            for repo in repos:
                repo_name = repo['name']
                clone_url = repo['clone_url']
                
                logger.debug(f"Repo found: {repo_name}")
                
                # create path for repo
                target_dir = os.path.join(username, f"{repo_name}.git")

                logger.debug("Cloning repo {clone_url}")
                try:
                    subprocess.run(
                        ["git", "clone", "--mirror", clone_url, target_dir],
                        check=True
                    )
                except subprocess.CalledProcessError:
                    logger.error(f"Error while cloning {repo_name}")
                    fail_count += 1

                repos_count += 1
            page += 1

        except requests.exceptions.RequestException as e:
            logger.error(f"Connection error: {e}")
            fail_count = 999
            break

    return repos_count, fail_count


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='github-backup - script to make backup of public GitHub repositories')

    parser.add_argument(
        '-v', '--verbose', required=False,
        default=False, action='store_true',
        help="Provide verbose output")
    parser.add_argument(
        '-u', '--user', required=True,
        default="rozie",
        help="GitHub user name"
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    # set verbosity
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    user = args.user
    repos_count, fail_count = clone_all_repos(user)
    logger.debug(f"Fetched {repos_count} repositories to '{user}/'")
    if fail_count:
        logger.error("{fail_count} errors occured")


if __name__ == '__main__':
    main()
