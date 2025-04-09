[![coverage](https://github.com/tagdots-dev/public201/actions/workflows/cron-coverage.yaml/badge.svg)](https://github.com/tagdots-dev/public201/actions/workflows/cron-coverage.yaml) [![update hooks](https://github.com/tagdots-dev/public201/actions/workflows/cron-update-hooks.yaml/badge.svg)](https://github.com/tagdots-dev/public201/actions/workflows/cron-update-hooks.yaml)

# Pre-Commit-Update-Hooks

## 😎 Why should you care?
**pre-commit** helps you improve code quality and flag problems before commit enters your repository.  If you have more than a handful of repositories in your organization, **Pre-Commit-Update-Hooks** helps you manage pre-commit hooks update efficiently.


#### Prerequisites
```
* 🐍 Python (3.x) (with virtualenv)
* 🧰 GH_TOKEN=<your GitHub Token> (as an environment variable)
    - require permissions to read contents and write pull request
    - fine-grained personal access token is recommended
```

<br>

### ⚡️ Build and Install Pre-Commit-Update-Hooks (mac)

```
git clone https://github.com/tagdots/pre-commit-update-hooks
cd pre-commit-update-hooks
mkvirtualenv update-hooks
workon update-hooks
python -m pip install -I build
python -m build
python -m pip install -e .
```

<br>

### 🔍 Using Pre-Commit-Update-Hooks
Show version
```
$ update-hooks --version
update-hooks, version 1.0.0
```

<br>

Shows command line options
```
$ update-hooks --help

Usage: update-hooks [OPTIONS]

Options:
  --file TEXT        <file> (default: .pre-commit-config.yaml)
  --dry-run BOOLEAN  <true, false> (default: true).
  --cleanup INTEGER  Cleanup after CI Test PRs created (default: 60).
  --version          Show the version and exit.
  --help             Show this message and exit.
```

<br>

With dry-run being true, **update-hooks** reads **.pre-commit-config.yaml** and produces a list of pre-commit hooks to update.
```
$ update-hooks --dry-run true

Starting update-hooks on .pre-commit-config.yaml (dry-run True)...

hadolint/hadolint (v2.11.0) is not using the latest release rev (v2.12.0)
pycqa/flake8 (7.1.2) is not using the latest release tag (7.2.0)
antonbabenko/pre-commit-terraform (v1.98.0) is not using the latest release rev (v1.98.1)

Update to pre-commit hooks: None
```

<br>

With dry-run being true, **update-hooks** reads **.pre-commit-config.yaml**, produces a list of pre-commit hooks to update, updates revs in **.pre-commit-config.yaml**, and creates a pull request.
```
$ update-hooks --dry-run false

Starting update-hooks on .pre-commit-config.yaml (dry-run False)...

hadolint/hadolint (v2.11.0) is not using the latest release rev (v2.12.0)
pycqa/flake8 (7.1.2) is not using the latest release tag (7.2.0)
antonbabenko/pre-commit-terraform (v1.98.0) is not using the latest release rev (v1.98.1)
Update to .pre-commit-config.yaml is successfully completed

Checkout new branch successfully....

Push commits successfully:
from local branch: update_hooks_01JR6JB1NENDM6FKJ5TZMFVMBE
with commit hash : 52044a23a14a6c515532b830c4b68a4d934cd838

Creating a Pull Request as follows:
Owner/Repo.  : tagdots/pre-commit-update-hooks
Purpose      : update pre-commit hooks version
Source Branch: tagdots:update_hooks_01JR6JB1NENDM6FKJ5TZMFVMBE
PR for Branch: main
Rev Variances: [{"owner_repo": "hadolint/hadolint", "current_rev": "v2.11.0", "new_rev": "v2.12.0"}, {"owner_repo": "pycqa/flake8", "current_rev": "7.1.2", "new_rev": "7.2.0"}, {"owner_repo": "antonbabenko/pre-commit-terraform", "current_rev": "v1.98.0", "new_rev": "v1.98.1"}]
Created pull request #101 successfully:  https://github.com/tagdots/pre-commit-update-hooks/pull/101
```

<br>

### 🙏  Contributing

- Fork this repository and create pull requests.
- Create an issue

<br>

### 📚 References

[Pre-Commit on Github](https://github.com/pre-commit/pre-commit-hooks)

[Fork this repo to create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

[Manage Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

<br>

### 📖 License

See [LICENSE](LICENSE).
