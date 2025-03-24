#!/usr/bin/env python

"""
1. extract repo url and rev from .pre-commit-config.yaml
2. get latest release or tag for each repo and compare them with the current rev
3. update .pre-commit-config.yaml
4. create a commit and pull request
5. create a Dockerfile
6. create tests and run in github actions
7. create a cron job to run in github actions
"""
import os

import yaml
from github import Github


github_token = os.environ.get("GH_TOKEN")
g = Github(github_token)

with open('.pre-commit-config.yaml', 'r') as f:
    data = yaml.safe_load(f)

    for r in data['repos']:
        # from .pre-commit-config.yaml
        # - repository name: r['repo']
        # - current release: r['rev']
        owner_repo = '/'.join(r['repo'].rsplit('/', 2)[-2:]).replace('.git', '')
        try:
            try:
                repo = g.get_repo(owner_repo)
                if not repo.get_latest_release():
                    print("Error: unknown issue to get the latest release.")
                else:
                    # https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#get-the-latest-release
                    # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L3597-L3603
                    # https://github.com/PyGithub/PyGithub/blob/main/github/GitRelease.py#L107

                    latest_release = repo.get_latest_release()
                    if r['rev'] == latest_release.tag_name:
                        print('current rev is the latest; DO NOTHING\n')
                    else:
                        print('current rev is not the latest.')
                        print(f"latest rev:  {latest_release.tag_name}; DO SOMETHING\n")

            except Exception as e:
                if f"{e.status}" == "404":
                    # https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-tags
                    # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L3568-L3573
                    # https://github.com/PyGithub/PyGithub/blob/main/github/Tag.py#L80-L82

                    print(f"{r['repo']} may not use releases.")
                    tags = repo.get_tags()
                    tag = next(x for x in repo.get_tags() if ("beta") not in x.name)

                    if r['rev'] == tag.name:
                        print('current rev is the latest; DO NOTHING\n')
                    else:
                        print('current rev is not the latest')
                        print(f"latest rev: {tag.name}; DO SOMETHING\n")
                else:
                    print(f"Error: {e}.")

        except Exception as e:
            print(f"Error: {e}.")
