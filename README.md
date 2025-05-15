[![coverage](https://github.com/tagdots-dev/public201/actions/workflows/cron-coverage.yaml/badge.svg)](https://github.com/tagdots-dev/public201/actions/workflows/cron-coverage.yaml) [![update-pre-commit](https://github.com/tagdots-dev/public201/actions/workflows/cron-update-pre-commit.yaml/badge.svg)](https://github.com/tagdots-dev/public201/actions/workflows/cron-update-pre-commit.yaml)

# Update-Pre-Commit

## 😎 Purpose
**Update-Pre-Commit** reads .pre-commit-config.yaml and create a pull request on Github.


#### Prerequisites
```
* 🐍 Python (3.12+) (with virtualenv)
* 🧰 export GH_TOKEN=<your GitHub Token>
    - fine-grained personal access token is recommended
    - require write permissions to contents and pull request
```

<br>

### ⚡️ Build and Install Update-Pre-Commit

```
git clone https://github.com/tagdots/update-pre-commit
cd update-pre-commit
mkvirtualenv update-pre-commit
make build
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

With dry-run being false, **update-pre-commit** reads **.pre-commit-config.yaml**, updates hooks rev in **.pre-commit-config.yaml**, and creates a pull request.
```
$ update-pre-commit --dry-run false

Starting update-pre-commit on .pre-commit-config.yaml (dry-run False)...

antonbabenko/pre-commit-terraform (v1.98.1) is not using the latest release rev (v1.99.0)
adrienverge/yamllint (v1.37.0) is not using the latest release rev (v1.37.1)

Update revs in .pre-commit-config.yaml: Success

Checkout new branch successfully....

Push commits successfully:
from local branch: update_pre_commit_01JV8P09N4G5K9Q4DDD533ARBH
with commit hash : 7b293faf5e14f6950bf28b510eb8d8c8beff26fe

Creating a Pull Request as follows:
Owner/Repo.  : tagdots/update-pre-commit
Title        : update pre-commit-config
Source Branch: tagdots:update_pre_commit_01JV8P09N4G5K9Q4DDD533ARBH
PR for Branch: main
Rev Variances: [{"owner_repo": "antonbabenko/pre-commit-terraform", "current_rev": "v1.98.1", "new_rev": "v1.99.0"}, {"owner_repo": "adrienverge/yamllint", "current_rev": "v1.37.0", "new_rev": "v1.37.1"}]
Created pull request #101 successfully: https://github.com/tagdots/update-pre-commit/pull/101
```

<br>

### 🙏  Contributing

- Fork this repository and create pull requests
- Create an [issue](https://github.com/tagdots/update-pre-commit/issues)

<br>

### 📚 References

[Pre-Commit on Github](https://github.com/pre-commit/pre-commit-hooks)

[How to fork a repo to create a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

[Manage Github Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

<br>

### 📖 License

See [LICENSE](LICENSE).
