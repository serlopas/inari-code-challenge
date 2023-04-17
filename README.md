# Inari Code Challenge


---

## Urls

- Local: http://localhost:8030/docs
---

## Development

### Project startup steps
#### 1) .env file

Generate your own **.env** file for development:
```sh
$ cp .env.default .env
```
Note: please do not use default `API_KEY=secure_api_key` in production

#### 2) Poetry lock
Generate **poetry.lock** file:
```sh
# 1) Jump to src/ directory
$ cd src
# 2) Then run
/src$ poetry lock
```

#### 3) Build docker-compose
```sh
# 1) Go back to project root
/src$ cd ..
# 2) run build command
$ docker-compose build
```
#### 4) Run docker-compose
```sh
$ docker-compose up
```
The server is going to be running on http://localhost:8030/docs. You can change the port number in `docker-compose.yml`
file:
```yaml
version: "3.7"

services:
  inari-code-challenge.api:
    # ...
    ports:
      - "8030:80"

```

### Pre-commit

```sh
$ pre-commit install
```

Hooks:

- trailing-whitespace
- end-of-file-fixer
- black
- flake8

---
## Api Version

Get version
```poetry version -s```

### How to bump version

Poetry `version` command is used to bump versions in this project

 - Patch: ```poetry version patch```
```
➜  src poetry version patch
Bumping version from 0.0.0 to 0.0.1
poetry_bumpversion: processed file app/settings/base.py
➜  src
```
 - Minor: ```poetry version minor```
```
➜  src poetry version minor
Bumping version from 0.0.0 to 0.1.0
poetry_bumpversion: processed file app/settings/base.py
➜  src
```
 - Major: ```poetry version major```
```
➜  src poetry version major
Bumping version from 0.0.0 to 1.0.0
poetry_bumpversion: processed file app/settings/base.py
➜  src
```
 - Specific version: ```poetry version 4.4.4```
```
➜  src poetry version 4.4.4
Bumping version from 0.0.0 to 4.4.4
poetry_bumpversion: processed file app/settings/base.py
➜  src
```

*plugin used to maintain the same version in all the code:* https://github.com/monim67/poetry-bumpversion

Files where version is defined:
- `src/pyproject.toml`
- `src/app/settings/base.py`

---

## Security


### Dependabot
Checks **python** and **docker** vulnerabilities.

Configuration file: `.github/dependabot.yml`
### Bandit
Static python code security analysis

Configuration on: `src/pyproject.toml` by tag:
```toml
[tool.bandit]
exclude_dirs = ["tests"]
```

Running in github-actions:

```yml
- name: Bandit security check
run: |
  bandit -r app/ -n 3 -ll
```
