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
        return Github(os.environ['GH_TOKEN'])
    except KeyError as e:
        print(f'Key Error: {e}')


def get_owner_repo(file):
    """
    create a repos_revs_list that captures all <owner/repo> and <rev>
    """
    repos_revs_list = []
    try:
        with open(f'{file}', 'r') as f:
            data = yaml.safe_load(f)

            for r in data['repos']:
                each_repo_rev_dict = {}
                owner_repo = '/'.join(r['repo'].rsplit('/', 2)[-2:]).replace('.git', '')
                current_rev = r['rev']
                each_repo_rev_dict.update(owner_repo=owner_repo, current_rev=current_rev)
                repos_revs_list.append(each_repo_rev_dict)
            return repos_revs_list
    except yaml.parser.ParserError as e:
        print(f'Invalid YAML file - {e}')
    except Exception as e:
        print(f'Exception Error to get owner/repo: {e}.')


def get_rev_variances(gh, variance_list, repos_revs_list):
    """
    capture differences between current rev and latest rev for each repo
    """
    for r in repos_revs_list:
        try:
            repo = gh.get_repo(r['owner_repo'])
            owner_repo = r['owner_repo']
            current_rev = r['current_rev']
            latest_release = repo.get_latest_release()
            if not current_rev == latest_release.tag_name:
                print(f'{owner_repo} ({current_rev}) is not using the latest release rev ({latest_release.tag_name})')
                add_variance_to_dict(owner_repo, current_rev, latest_release.tag_name, variance_list)

        except Exception as e:
            if f'{e.status}' == "404":
                tag = next(x for x in repo.get_tags() if ("beta" and "alpha" and "rc") not in x.name)
                if not current_rev == tag.name:
                    print(f'{owner_repo} ({current_rev}) is not using the latest release tag ({tag.name})')
                    add_variance_to_dict(owner_repo, current_rev, tag.name, variance_list)


def add_variance_to_dict(owner_repo, current_rev, new_rev, variance_list):
    variance_dict = {}
    variance_dict.update(owner_repo=owner_repo, current_rev=current_rev, new_rev=new_rev)
    variance_list.append(variance_dict)


def update_pre_commit(file, variance_list):
    """
    update pre-commit configuration file
    """
    # try:
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

    print(f'Update to {file} is successfully completed')


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
    print('Checkout new branch successfully....')
    return owner_repo, repo_obj_branch_name


def push_commit(file, active_branch_name):
    """
    push commits to remote
    """
    repo_path = os.getcwd()
    branch = active_branch_name
    message = 'update pre-commit hooks version'
    files_to_stage = [file]

    repo_obj = git.Repo(repo_path)
    repo_obj.index.add(files_to_stage)  # other option ('*')
    repo_obj.index.write()
    commit = repo_obj.index.commit(message)
    repo_obj.git.push("--set-upstream", 'origin', branch)
    print('Push commits successfully:')
    print(f'from local branch: {branch}')
    print(f'with commit hash : {commit.hexsha}')


def create_pr(gh, owner_repo, active_branch_name, variance_list):
    """
    create Pull Request
    """
    owner = owner_repo.split('/')[0]
    repo = gh.get_repo(owner_repo)
    pr_base_branch = repo.default_branch
    pr_body = json.dumps(variance_list)
    pr_branch = f'{owner}:{active_branch_name}'
    pr_title = 'update pre-commit hooks version'

    print('Creating a Pull Request as follows:')
    print(f'Owner/Repo.  : {owner_repo}')
    print(f'Purpose      : {pr_title}')
    print(f'Source Branch: {pr_branch}')
    print(f'PR for Branch: {pr_base_branch}')
    print(f'Rev Variances: {pr_body}')
    try:
        pr = repo.create_pull(title=pr_title, body=pr_body, head=pr_branch, base=pr_base_branch)
        print(f'Created pull request #{pr.number} successfully: {pr.html_url}')
    except Exception as e:
        print(f'Exception Error to create PR: {e}')


@click.command()
@click.option('--file', required=False, default='.pre-commit-config.yaml', help='file (default: .pre-commit-config.yaml)')
@click.option('--dry-run', required=False, default=True, help='dry-run [true, false] (default: true).')
def main(file, dry_run):
    print(f"Starting update-hooks on {file} (dry-run {dry_run})...")
    try:
        variance_list = []
        gh = get_auth()
        repos_revs_list = get_owner_repo(file)
        get_rev_variances(gh, variance_list, repos_revs_list)

        if len(variance_list) > 0 and not dry_run:
            update_pre_commit(file, variance_list)
            owner_repo, active_branch_name = checkout_new_branch()
            push_commit(file, active_branch_name)
            create_pr(gh, owner_repo, active_branch_name, variance_list)
        else:
            print('Update to pre-commit hooks: None')
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
