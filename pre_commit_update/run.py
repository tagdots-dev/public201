#!/usr/bin/env python

"""
Purpose: update pre-commit configuration and create a pull request if necessary
"""

import json
import os
import sys

import click
import git
import ulid
import yaml
from github import Github


def get_auth():
    """
    github token required or GitHub API rate limit can kick in
    """
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


def get_owner_repo(file):
    """
    create a repos_revs_list that captures all <owner/repo> and <rev>
    """
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
    """
    capture differences between current rev and latest rev for each repo
    """
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
                    """ pre-commit hooks repo uses latest tag instead of github releases """
                    if f'{e.status}' == "404":
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
    """
    update pre-commit configuration file
    """
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


def checkout_new_branch():
    """
    create a git object to 1) create a new branch name 2) checkout this new branch
    """
    repo_path = os.getcwd()
    branch_suffix = ulid.new()
    repo_obj = git.Repo(repo_path)
    repo_obj_branch_name = repo_obj.create_head(f'update_hooks_{branch_suffix}')
    repo_obj_branch_name.checkout()
    repo_obj_remote_url = repo_obj.remotes.origin.url
    owner_repo = '/'.join(repo_obj_remote_url.rsplit('/', 2)[-2:]).replace('.git', '')
    print('\nCheckout new branch successfully....')
    return owner_repo, repo_obj_branch_name


def push_commit(file, active_branch_name):
    """
    push commits to remote
    """
    try:
        repo_path = os.getcwd()
        branch = active_branch_name
        message = 'update pre-commit hooks version'
        files_to_stage = [file]

        repo_obj = git.Repo(repo_path)
        repo_obj.index.add(files_to_stage)  # other option ('*')
        repo_obj.index.write()
        commit = repo_obj.index.commit(message)
        repo_obj.git.push("--set-upstream", 'origin', branch)
        print('\nPush commits successfully:')
        print(f'from local branch: {branch}')
        print(f'with commit hash : {commit.hexsha}')
    except Exception as e:
        print(f'\nException Error to push commit: {e}')


def create_pr(owner_repo, active_branch_name, default_branch, variance_list):
    """
    create Pull Request
    """
    owner = owner_repo.split('/')[0]
    repo = gh.get_repo(owner_repo)
    pr_base_branch = repo.default_branch
    pr_body = json.dumps(variance_list)
    pr_branch = f'{owner}:{active_branch_name}'
    pr_title = 'update pre-commit hooks version'

    print('\nCreating a Pull Request as follows:')
    print(f'Owner/Repo.  : {owner_repo}')
    print(f'Purpose      : {pr_title}')
    print(f'Source Branch: {pr_branch}')
    print(f'PR for Branch: {pr_base_branch}')
    print(f'Rev Variances: {pr_body}')
    try:
        pr = repo.create_pull(title=pr_title, body=pr_body, head=pr_branch, base=pr_base_branch)
        print(f'\nPull request created successfully: {pr.html_url}')
    except Exception as e:
        print(f'\nException Error to create PR: {e}')


@click.command()
@click.option('--file', required=False, default='.pre-commit-config.yaml', help='full file path.')
@click.option('--dry-run', required=True, default=True, help='dry-run=False will update config file')
@click.option('--default-branch', required=False, default='main', help='main is default branch')
def main(file, dry_run, default_branch):
    print(f"Starting autoupdate on {file} (dry-run {dry_run})...\n")
    try:
        global gh
        global variance_list
        variance_list = []
        gh = get_auth()
        repos_revs_list = get_owner_repo(file)
        get_rev_variances(file, repos_revs_list)

        if len(variance_list) > 0 and not dry_run:
            update_pre_commit(file, dry_run, variance_list)
            owner_repo, active_branch_name = checkout_new_branch()
            push_commit(file, active_branch_name)
            create_pr(owner_repo, active_branch_name, default_branch, variance_list)
        else:
            print('\nUpdate to pre-commit hooks: none')
    except Exception as e:
        print(f'\nException Error to autoupdate: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
