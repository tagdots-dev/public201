#!/usr/bin/env python

"""
Purpose: unit and integration tests
"""
import io
import os
import shutil
import sys
import time
import unittest
from unittest import mock

from click.testing import CliRunner
from github import Github

from update_pre_commit.run import (
    checkout_new_branch,
    create_pr,
    get_auth,
    get_owner_repo,
    get_rev_variances,
    main,
    push_commit,
    update_pre_commit_config,
)


class TestGetAuth(unittest.TestCase):
    ''' hold output from source script '''
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        sys.stderr = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    ''' env var GH_TOKEN complete successfully '''
    def test_get_auth_gh_token_success(self):
        self.assertIsInstance(get_auth(), Github)

    ''' assert mock env var GH_TOKEN not exists (KeyError)'''
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_get_auth_gh_token_notExist(self):
        self.assertIsNone(get_auth())

    ''' assert mock env var GH_TOKEN with invalid value '''
    @mock.patch.dict(os.environ, {'GH_TOKEN': 'github_pat_1234567890'}, clear=True)  # checkov:skip=CKV_SECRET_6
    def test_get_auth_gh_token_invalid(self):
        self.assertRaises(TypeError, get_auth())


class TestGetOwnerRepo(unittest.TestCase):
    file_isvalid = 'tests/files/pre-commit-config-isvalid.yaml'
    file_invalid = 'tests/files/pre-commit-config-invalid.yaml'
    file_noexist = 'tests/files/pre-commit-config-noexist.yaml'

    ''' hold output from source script '''
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        sys.stderr = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    ''' assert file exists = true '''
    def test_get_owner_repo_file_exists_true(self):
        self.assertTrue(os.path.exists(self.file_isvalid))

    ''' assert file exists = false '''
    def test_get_owner_repo_file_exists_false(self):
        self.assertFalse(get_owner_repo(self.file_noexist))

    ''' assert output is a list from valid file '''
    def test_get_owner_repo_return_list_success(self):
        function_output_should_be_list = get_owner_repo(self.file_isvalid)
        self.assertIsInstance(function_output_should_be_list, list)

    ''' assert output is NOT a list from an invalid file '''
    def test_get_owner_repo_return_list_failure(self):
        function_output_should_be_list = get_owner_repo(self.file_invalid)
        self.assertNotIsInstance(function_output_should_be_list, list)


class TestGetRevVariances(unittest.TestCase):
    ''' hold output from source script '''
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        sys.stderr = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    repos_rev_list = [
        {'owner_repo': 'adrienverge/yamllint', 'current_rev': 'v1.37.0'},
        {'owner_repo': 'pre-commit/pre-commit-hooks', 'current_rev': 'v4.0.0'},
        {'owner_repo': 'pycqa/flake8', 'current_rev': '7.1.2'}
    ]

    def test_get_rev_variances_to_dict(self):
        variance_list = []
        for r in self.repos_rev_list:
            result = get_rev_variances(get_auth(), variance_list, r['owner_repo'], r['current_rev'])
        assert type(result) is not None


class TestUpdatePreCommit(unittest.TestCase):
    file_isvalid_src = 'tests/files/pre-commit-config-isvalid.yaml'
    file_isvalid_dst = 'tests/files/pre-commit-config-isvalid-temp.yaml'
    variance_list = [
        {'owner_repo': 'pycqa/flake8', 'current_rev': '7.1.2', 'new_rev': '7.2.0'},
        {'owner_repo': 'pre-commit/pre-commit-hooks', 'current_rev': 'v4.0.0', 'new_rev': 'v5.0.0'}
    ]

    ''' hold output from source script '''
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        sys.stderr = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    ''' assert output is a list after update_pre_commit '''
    def test_update_pre_commit_return_list_success(self):
        shutil.copyfile(self.file_isvalid_src, self.file_isvalid_dst)
        update_pre_commit_config(self.file_isvalid_dst, self.variance_list)
        function_output_should_be_list = get_owner_repo(self.file_isvalid_dst)
        self.assertIsInstance(function_output_should_be_list, list)
        os.remove(self.file_isvalid_dst)


class TestWritePR(unittest.TestCase):
    cleanup = 30
    file_isvalid = 'tests/files/pre-commit-config-isvalid.yaml'
    msg_suffix = '[CI - Testing]'
    variance_list = [
        {'owner_repo': 'pycqa/flake8', 'current_rev': '7.1.2', 'new_rev': '7.2.0'},
        {'owner_repo': 'pre-commit/pre-commit-hooks', 'current_rev': 'v4.0.0', 'new_rev': 'v5.0.0'}
    ]

    ''' hold output from source script '''
    def setUp(self):
        self.held_output = io.StringIO()
        sys.stdout = self.held_output
        sys.stderr = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def test_create_pr_success(self):
        gh = get_auth()
        owner_repo, active_branch_name = checkout_new_branch()
        push_commit(self.file_isvalid, active_branch_name, self.msg_suffix)
        pr_number = create_pr(gh, owner_repo, active_branch_name, self.variance_list, self.msg_suffix)
        self.assertIsInstance(pr_number, int)

        ''' clean up after above '''
        ''' ^^ may have error if it takes more than the time.sleep seconds to get PR ready '''
        repo = gh.get_repo(owner_repo)
        pull = repo.get_pull(pr_number)
        ref = repo.get_git_ref(f"heads/{active_branch_name}")
        time.sleep(self.cleanup)
        pull.edit(state="closed")
        ref.delete()


class TestZMain(unittest.TestCase):
    valid_file = 'tests/files/pre-commit-config-isvalid.yaml'

    def setUp(self):
        self.runner = CliRunner()

    ''' assert zero exit code with cleanup option success '''
    def test_main_cleanup_option_success(self):
        result = self.runner.invoke(main, ['--cleanup', 45])
        self.assertEqual(result.exit_code, 0)

    ''' assert zero exit code with cleanup option failure '''
    def test_main_cleanup_option_failure(self):
        result = self.runner.invoke(main, ['--cleanup', 'hello'])
        self.assertNotEqual(result.exit_code, 0)

    ''' assert zero exit code with dry-run false '''
    def test_main_dry_run_false_success(self):
        result = self.runner.invoke(main, ['--dry-run', 'False'])
        # print(result.stdout)
        self.assertEqual(result.exit_code, 0)

    ''' assert zero exit code with dry-run true with a valid file '''
    def test_main_dry_run_true_failure(self):
        result = self.runner.invoke(main, ['--file', self.valid_file])
        self.assertEqual(result.exit_code, 0)

    ''' assert zero exit code with dry-run true '''
    def test_main_dry_run_true_success(self):
        result = self.runner.invoke(main, ['--dry-run', 'True'])
        self.assertEqual(result.exit_code, 0)

    ''' assert non-zero exit code with dry-run typo '''
    def test_main_dry_run_typo_failure(self):
        result = self.runner.invoke(main, ['--dry-run', 'Typo'])
        self.assertNotEqual(result.exit_code, 0)

    ''' assert non-zero exit code with non-existent file '''
    def test_main_file_not_exist_failure(self):
        result = self.runner.invoke(main, ['--file', 'file-not-exist.yaml'])
        self.assertNotEqual(result.exit_code, 0)

    ''' assert non-zero exit code with an invalid option '''
    def test_main_invalid_option_failure(self):
        result = self.runner.invoke(main, ['--hello', 'world'])
        self.assertNotEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main()
