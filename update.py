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

- file root folder (default)
- file somewhere else
"""

import os
import sys

import click
# import ulid
import yaml
from github import Github


def get_auth():
    """ github token required or GitHub API rate limit can kick in """
    try:
        github_token = os.environ['GH_TOKEN']
        if len(github_token) >= 40 or github_token.startswith('github_pat_'):
            gh = Github(github_token)
            return gh
        else:
            raise AssertionError
    except KeyError:
        print('Key Error: Environment variable (GH_TOKEN) is not found')
    except AssertionError:
        print('Assertion Error: Environment variable (GH_TOKEN) is not valid')
        sys.exit(1)
    else:
        print('Got Github Token successfully.\n')


def get_owner_repo(file, gh):
    try:
        repos_revs_list = []
        with open(f'{file}', 'r') as f:
            data = yaml.safe_load(f)

        for r in data['repos']:
            each_repo_rev_dict = {}
            owner_repo = '/'.join(r['repo'].rsplit('/', 2)[-2:]).replace('.git', '')
            current_rev = r['rev']
            each_repo_rev_dict.update(owner_repo=owner_repo, current_rev=current_rev)
            repos_revs_list.append(each_repo_rev_dict)
        return repos_revs_list

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


def get_rev_variances(file, repos_revs_list):
    try:
        for r in repos_revs_list:
            try:
                repo = gh.get_repo(r['owner_repo'])
                owner_repo = r['owner_repo']
                current_rev = r['current_rev']
                latest_release = repo.get_latest_release()
                if not current_rev == latest_release.tag_name:
                    print(f'{owner_repo} ({current_rev}) is not using the latest rev ({latest_release.tag_name})')
                    add_variance_to_dict(owner_repo, current_rev, latest_release.tag_name)

            except NameError as n:
                print(f"NameError: {n}")
            except TypeError as t:
                print(f'TypeError: {t}')
            except Exception as e:
                if f'{e.status}':
                    if f'{e.status}' == "404":
                        """ pre-commit hooks repo uses latest tag instead of github releases """
                        try:
                            tag = next(x for x in repo.get_tags() if ("beta" and "alpha") not in x.name)
                            if not current_rev == tag.name:
                                print(f'{owner_repo} ({current_rev}) is not using the latest rev ({tag.name})')
                                add_variance_to_dict(owner_repo, current_rev, tag.name)

                        except Exception as e:
                            print(f'Exception Error to get latest tag: {owner_repo} - {e}')
                    else:
                        print(f'Exception Error to get rev variances: {owner_repo} {e}.')
                else:
                    print(f'Exception Error to get rev variances: {owner_repo} {e}.')

    except Exception as e:
        print(f'Exception Error to get rev variances: {owner_repo} {e}.')


def add_variance_to_dict(owner_repo, current_rev, new_rev):
    variance_dict = {}
    variance_dict.update(owner_repo=owner_repo, current_rev=current_rev, new_rev=new_rev)
    variance_list.append(variance_dict)


def update_pre_commit(file, dry_run, variance_list):
    if len(variance_list) > 0 and not dry_run:
        try:
            with open(file, 'r') as f:
                data = yaml.safe_load(f)

            x = len(data['repos'])
            for i in range(x):
                for variance_dict in variance_list:
                    if variance_dict['owner_repo'] in data['repos'][i]['repo'] and \
                            variance_dict['current_rev'] in data['repos'][i]['rev']:
                        data['repos'][i]['rev'] = variance_dict['new_rev']

            with open(file, 'w') as f:
                yaml.dump(data, f, indent=2, sort_keys=False)
            print(f'\nUpdate to {file} is successfully completed')

        except Exception as e:
            print(f'Exception Error: {e}')
    else:
        print(f'\nThere is no update to {file}.')


def stage_change(gh, file, repos_revs_list, variance_list):
    try:
        repo = gh.get_repo("tagdots-dev/public201")
        # stage_file_branch_suffix = ulid.new()
        # branch = f'update/pre-commit-hooks-{stage_file_branch_suffix}'
        # title = f'update pre-commit hooks version at {file}'
        message = 'update pre-commit hooks version'
        # body = variance_list

        # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2374-L2403
        file_contents = repo.get_contents(file)

        with open(file, 'r') as f:
            file_contents_read = f.read()

        # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2743-L2801
        stage_change_result = repo.update_file(file, message, file_contents_read, file_contents.sha)
        print(stage_change_result)

    except Exception as e:
        print(f'Exception Error: {e}')


@click.command()
@click.option('--file', required=False, default='./.pre-commit-config.yaml', help='full file path.')
@click.option('--dry-run', required=True, default=True, help='dry-run=False will update config file')
def main(file, dry_run):
    print(f"Starting autoupdate on {file} (dry-run={dry_run})...\n")
    try:
        global gh
        global variance_list
        variance_list = []
        gh = get_auth()
        repos_revs_list = get_owner_repo(file, gh)
        get_rev_variances(file, repos_revs_list)
        update_pre_commit(file, dry_run, variance_list)

        if dry_run is False and len(variance_list) > 0:
            stage_change(gh, file, repos_revs_list, variance_list)

    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
