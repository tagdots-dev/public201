#!/usr/bin/env python

"""
0. get auth token
1. extract repo url and rev from .pre-commit-config.yaml
2. get latest release or tag for each repo and compare them with the current rev

3. update .pre-commit-config.yaml
4. create a commit and pull request

5. create a Dockerfile
6. create tests and run in github actions
7. create a cron job to run in github actions

options:
- dry-run (default)
- no-dry-run

- location root (default)
- location somewhere else
"""

# import json
# import logging
import os
# import pprint
import sys

import click
import yaml
from github import Github


def get_auth():
    """ github token required as GitHub API rate limit kicks in quickly """
    global gh
    try:
        github_token = os.environ['GH_TOKEN']
        if len(github_token) >= 40 or github_token.startswith('github_pat_'):
            gh = Github(github_token)
        else:
            raise AssertionError
    except KeyError:
        print('Key Error: Environment variable (GH_TOKEN) is not found')
    except AssertionError:
        print('Assertion Error: Environment variable (GH_TOKEN) is not valid')
        sys.exit(1)
    else:
        print('Got Github Token successfully.\n')


def get_owner_repo(file):
    try:
        with open(f'{file}', 'r') as f:
            data = yaml.safe_load(f)
            for r in data['repos']:
                # from .pre-commit-config.yaml
                owner_repo = '/'.join(r['repo'].rsplit('/', 2)[-2:]).replace('.git', '')
                current_rev = r['rev']
                get_rev_variances(file, data, owner_repo, current_rev)

    except FileNotFoundError as f:
        print(f'File Not Found Error: {f}.')
    except yaml.scanner.ScannerError as s:
        print(f'Yaml Format Error: {s}.')
    except yaml.parser.ParserError as p:
        print(f'File Parse Error: {p}.')
    except KeyError as k:
        print(f'Missing Key Error: {k}.')
    except Exception as e:
        print(f'Exception Error to get owner/repo: {e}.')


def get_rev_variances(file, data, owner_repo, current_rev):
    try:
        try:
            repo = gh.get_repo(owner_repo)
            latest_release = repo.get_latest_release()
            if not current_rev == latest_release.tag_name:
                print(f'{owner_repo} ({current_rev}) is not using the latest rev ({latest_release.tag_name}); DO SOMETHING')
                update_config(file, data, latest_release.tag_name)

        except NameError as n:
            print(f"NameError: {n}")
        except Exception as e:
            if f"{e.status}" == "404":
                """ repo uses latest tag instead of github releases """
                get_latest_tag(file, data, repo, owner_repo, current_rev)
            else:
                print(f'Exception Error to get rev variances: {owner_repo} {e}.')

    except Exception as e:
        print(f'Exception Error to get rev variances: {owner_repo} {e}.')


def get_latest_tag(file, data, repo, owner_repo, current_rev):
    try:
        # tags = repo.get_tags()
        tag = next(x for x in repo.get_tags() if ("beta" and "alpha") not in x.name)

        if not current_rev == tag.name:
            print(f'{owner_repo} ({current_rev}) is not using the latest rev ({tag.name}); DO SOMETHING')
            update_config(file, data, tag.name)

    except Exception as e:
        print(f'Exception Error to get latest tag: {owner_repo} - {e}')


def update_config(file, data, tag_name):
    # if 'repos' in data and 'rev' in data['repos'][0] and 'repo' in data['repos'][0]:
    #     data['repos'][0]['rev'] = tag_name

    # with open(file, 'w', encoding='utf-8') as file:
    #     yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
    print("test")


@click.command()
@click.option('--file', required=False, default='./.pre-commit-config.yaml', help='full file path.')
@click.option('--dry-run', required=True, default=True, help='dry-run=False will update config file')
def main(file, dry_run):
    print(f"Starting autoupdate on {file} (dry-run={dry_run})...\n")
    try:
        get_auth()
        get_owner_repo(file)
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
