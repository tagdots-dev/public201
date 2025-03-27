#!/usr/bin/env python

"""
Purpose: update .pre-commit-config.yaml and create a PR
"""

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
    repo_obj_branch_name = repo_obj.create_head(f'update/hooks_{branch_suffix}')
    repo_obj_branch_name.checkout()
    repo_obj_remote_url = repo_obj.remotes.origin.url
    owner_repo = '/'.join(repo_obj_remote_url.rsplit('/', 2)[-2:]).replace('.git', '')
    return owner_repo, repo_obj_branch_name


def push_commit(gh, file, active_branch_name):
    """
    push commits to remote
    """
    try:
        repo_path = os.getcwd()
        branch = active_branch_name
        message = 'update pre-commit hooks version'
        files_to_stage = [file, 'update.py']

        repo_obj = git.Repo(repo_path)
        repo_obj.index.add(files_to_stage)  # other option ('*')
        repo_obj.index.write()
        commit = repo_obj.index.commit(message)
        push = repo_obj.git.push("--set-upstream", 'origin', branch)
        print(f'from local branch: {branch}')
        print(f'push commit hash : {commit.hexsha}')
        print(push)

    except Exception as e:
        print(f'Exception Error to push commit: {e}')


def create_pr(gh, owner_repo, active_branch_name, default_branch, variance_list):
    """
    create Pull Request
    """
    repo = gh.get_repo(owner_repo)
    pr_base_branch = default_branch
    # pr_body = variance_list
    pr_body = 'test'
    pr_branch = active_branch_name
    pr_title = 'update pre-commit hooks version'

    try:
        pr = repo.create_pull(title=pr_title, body=pr_body, head=pr_branch, base=pr_base_branch)
        print(f"Pull request created successfully: {pr.html_url}")
    except Exception as e:
        print(f"Exception Error to create PR: {e}")


def cleanup(active_branch_name):
    """
    remove local branch
    """
    print('test')


@click.command()
@click.option('--file', required=False, default='./.pre-commit-config.yaml', help='full file path.')
@click.option('--dry-run', required=True, default=True, help='dry-run=False will update config file')
@click.option('--default-branch', required=False, default='main', help='main is default branch')
def main(file, dry_run, default_branch):
    print(f"Starting autoupdate on {file} (dry-run={dry_run})...\n")
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
            push_commit(gh, file, active_branch_name)
            create_pr(gh, owner_repo, active_branch_name, default_branch, variance_list)
            cleanup(active_branch_name)

    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()

# from github import Github
# import os
# github_token = os.environ['GH_TOKEN']
# global gh
# gh = Github(github_token)
# repo = gh.get_repo("tagdots-dev/public201")

# file = 'test_pre-commit.yaml'
# contents = repo.get_contents(path=file, ref="test-01")
# final_contents = contents.decoded_content.decode()
# stage_change_result = repo.update_file(contents.path, 'update hooks', final_contents, contents.sha)

###########################################################
# def stage_change(gh, file, repos_revs_list, variance_list):
#     # try:
#     repo = gh.get_repo("tagdots-dev/public201")
#     # stage_file_branch_suffix = ulid.new()
#     # branch = f'update/pre-commit-hooks-{stage_file_branch_suffix}'
#     branch_name = "test-01"
#     # title = f'update pre-commit hooks version at {file}'
#     message = 'update pre-commit hooks version'
#     # body = variance_list

#     # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2374-L2403
#     contents = repo.get_contents(path=file, ref="test-01")
#     final_contents = contents.decoded_content.decode()

#     # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2743-L2801
#     stage_change_result = repo.update_file(contents.path, message, final_contents, contents.sha, branch=branch_name)
#     # stage_change_result = repo.update_file(contents.path, message, final_contents, contents.sha)
#     print(stage_change_result)

#     # except github.GithubException.GithubException as e:
#     #     print(f'Github Exception: {e}')
###########################################################
# def stage_change(gh, file, repos_revs_list, variance_list):
#     # try:
#     repo = gh.get_repo("tagdots-dev/public201")
#     print("1")
#     # stage_file_branch_suffix = ulid.new()
#     # branch = f'update/pre-commit-hooks-{stage_file_branch_suffix}'
#     branch = "test-01"
#     # title = f'update pre-commit hooks version at {file}'
#     message = 'update pre-commit hooks version'
#     # body = variance_list

#     # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2374-L2403
#     file_contents = repo.get_contents(path=file, ref="test-01")
#     print("2")
#     print(file_contents)

#     with open(file, 'r') as f:
#         file_contents_read = f.read()
#     print("3")

#     # https://github.com/PyGithub/PyGithub/blob/main/github/Repository.py#L2743-L2801
#     stage_change_result = repo.update_file(file, message, file_contents_read, file_contents.sha, branch)
#     print(stage_change_result)

#     # except Exception:
#     #     print(f'test')

# def stage_change(gh, file):
#     print(gh)
#     # get ref
#     ref = repo.get_git_ref("heads/test-01")
#     print(ref)

#     # get the parent commit
#     parent_commit = repo.get_git_commit(ref.object.sha)
#     print(parent_commit)

#     # file to create a commit
#     # file (already part of command argument)
#     contents = repo.get_contents(path=file)
#     print(content.path)

#     # create a new tree with the new file content
#     tree = [
#         {
#             "path": file,
#             "mode": "100644",
#             "type": "blob",
#             "content": contents
#         }
#     ]
#     new_tree = repo.create_git_tree([tree], parent_tree=parent_commit.tree)
#     print(new_tree)

#     # Create a new commit
#     message = 'update pre-commit hooks version'
#     commit = repo.create_git_commit(
#         message, new_tree.sha, [parent_commit]
#     )
#     print(commit)

#     # Update the reference to point to the new commit
#     ref.edit(commit.sha, force=True)


# import git

# repo_path = '/path/to/your/repository'

# try:
#     repo = git.Repo(repo_path)
#     # 暂存所有修改的文件
#     repo.git.add(all=True)
#     commit_message = 'Stage and commit all changes'
#     commit = repo.index.commit(commit_message)
#     print(f"成功创建提交，提交哈希: {commit.hexsha}")
# except git.InvalidGitRepositoryError:
#     print(f"指定的路径 {repo_path} 不是一个有效的 Git 仓库。")
# except Exception as e:
#     print(f"发生错误: {e}")
