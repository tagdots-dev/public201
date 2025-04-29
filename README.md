[![coverage](https://github.com/tagdots/update-pre-commit/actions/workflows/cron-coverage.yaml/badge.svg)](https://github.com/tagdots/update-pre-commit/actions/workflows/cron-coverage.yaml) [![update-pre-commit](https://github.com/tagdots/update-pre-commit/actions/workflows/cron-update-pre-commit.yaml/badge.svg)](https://github.com/tagdots/update-pre-commit/actions/workflows/cron-update-pre-commit.yaml)

# Update-Pre-Commit

## 😎 Purpose
**Update-Pre-Commit** reads .pre-commit-config.yaml and create a pull request on Github.


#### Prerequisites
```
* 🐍 Python (3.12+) (with virtualenv)
* 🧰 export GH_TOKEN=<your GitHub Token>
    - require permissions to write contents pull request
    - fine-grained personal access token is recommended
```

<br>

### ⚡️ Build and Install Update-Pre-Commit

```
git clone https://github.com/tagdots/update-pre-commit
cd update-pre-commit
mkvirtualenv update-pre-commit
workon update-pre-commit
python -m pip install -U build
python -m build
python -m pip install -e .
```

<br>

### 🔍 Using Update-Pre-Commit
Show version
```
$ update-pre-commit --version
update-pre-commit, version 1.0.0
```

<br>

Shows command line options
```
$ update-pre-commit --help

Usage: update-pre-commit [OPTIONS]

Options:
  --file TEXT        <file> (default: .pre-commit-config.yaml).
  --dry-run BOOLEAN  <true, false> (default: true).
  --cleanup INTEGER  Cleanup after CI Test PRs created (default: 90).
  --version          Show the version and exit.
  --help             Show this message and exit.
```

<br>

With dry-run being true by default, **update-pre-commit** reads **.pre-commit-config.yaml** and produces a list of pre-commit hooks to update.
```
$ update-pre-commit

Starting update-pre-commit on .pre-commit-config.yaml (dry-run True)...

hadolint/hadolint (v2.11.0) is not using the latest release rev (v2.12.0)
pycqa/flake8 (7.1.2) is not using the latest release tag (7.2.0)
antonbabenko/pre-commit-terraform (v1.98.0) is not using the latest release rev (v1.98.1)
Update pre-commit hooks: None
```

<br>

With dry-run being false, **update-pre-commit** reads **.pre-commit-config.yaml**, produces a list of pre-commit hooks to update, updates hooks rev in **.pre-commit-config.yaml**, and creates a pull request.
```
$ update-pre-commit --dry-run false

Starting update-pre-commit on .pre-commit-config.yaml (dry-run False)...

hadolint/hadolint (v2.11.0) is not using the latest release rev (v2.12.0)
pycqa/flake8 (7.1.2) is not using the latest release tag (7.2.0)
antonbabenko/pre-commit-terraform (v1.98.0) is not using the latest release rev (v1.98.1)
Update .pre-commit-config.yaml successfully

Checkout new branch successfully....

Push commits successfully:
from local branch: update_hooks_01JR6JB1NENDM6FKJ5TZMFVMBE
with commit hash : 52044a23a14a6c515532b830c4b68a4d934cd838

Creating a Pull Request as follows:
Owner/Repo.  : tagdots/update-pre-commit
Purpose      : update pre-commit hooks version
Source Branch: tagdots:update_hooks_01JR6JB1NENDM6FKJ5TZMFVMBE
PR for Branch: main
Rev Variances: [{"owner_repo": "hadolint/hadolint", "current_rev": "v2.11.0", "new_rev": "v2.12.0"}, {"owner_repo": "pycqa/flake8", "current_rev": "7.1.2", "new_rev": "7.2.0"}, {"owner_repo": "antonbabenko/pre-commit-terraform", "current_rev": "v1.98.0", "new_rev": "v1.98.1"}]
Created pull request #101 successfully:  https://github.com/tagdots/update-pre-commit/pull/101
```

<br>

### 🙏  Contributing

- Fork this repository and create pull requests.
- Create an [issue](https://github.com/tagdots/update-pre-commit/issues).

<br>

### 📚 References

[Pre-Commit on Github](https://github.com/pre-commit/pre-commit-hooks)

[How to fork a repo to create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

[Manage Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

<br>

### 📖 License

See [LICENSE](LICENSE).
