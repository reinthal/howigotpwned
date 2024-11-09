## v1.0.1 (2024-11-09)

### Fix

- **cit0day**: remove population of the dynamic partitions from the job as it causes partitions to fail

## v1.0.0 (2024-11-09)

### Feat

- **cit0day**: add schemas for table

## v0.8.0 (2024-11-09)

### Feat

- **dagster**: add ttl
- **cit0day**: add category
- **cit0day**: add domain and username veryfi with duckdb
- **cit0day**: add domain and username
- add sql interface

### Fix

- **dagster**: update dagster k8s config to clean up after itself

## v0.7.0 (2024-11-08)

### Feat

- **dev**: add harlequin for querying data

## v0.6.0 (2024-11-06)

### Feat

- **nessie**: add  how to connect to nessie

### Fix

- 10 is better
- add logging
- relax back off tries to 4 for early failure
- add seamless sops decryption of secrets
- update dagster credentials for destination s3
- minio source credentials

## v0.5.1 (2024-11-02)

### Fix

- remove kuberntes configuration

## v0.5.0 (2024-10-27)

### Feat

- handle latin-1 encodings

### Fix

- broken job

## v0.4.1 (2024-10-27)

### Fix

- downstream not up

## v0.4.0 (2024-10-27)

### Feat

- add nessie-cli
- add nessie branch

## v0.3.4 (2024-10-27)

### Fix

- limit concurrent runs to 5

## v0.3.3 (2024-10-26)

### Fix

- patch missed comma

## v0.3.2 (2024-10-26)

### Fix

- add description of cit0day staging asset
- add missing dagster postgres

## v0.3.1 (2024-10-26)

### Fix

- staging asset does not return a df it has side effects
- image repository
- add label to dockerfile and try to rebuild image

## v0.3.0 (2024-10-21)

### Feat

- add k8s executor

## v0.2.0 (2024-10-21)

### Feat

- add backoff strategy for concurrent writes
- add schedule

### Fix

- update linter settings, fix lint error
- cleanup of stale environment variables
- lint it!
- remove poc file from repo
- more linting
- linting

## v0.14.0 (2024-08-23)

### Feat

- add check to see if repo is template. (#9)

### Fix

- exit without error. (#10)

## v0.13.0 (2024-08-22)

### Fix

- merge commit pull from `feat: add nix flake`
- update docs for nix
- add missing dependency, add `export` for .envrc

## v0.12.0 (2024-08-22)

### Feat

- add nix flake
- add basic pandera checks for pokemon assets.

### Fix

- remove polars not used
- fix references and namings to pokemon

## v0.11.0 (2024-08-22)

### Feat

- change from swapi to pokemon (#7)
- add pandera checks for dlt assets.
- add custom Translator and SourceAsset to modify group name for dlt pipeline.
- add GitHub action to build and push images
- add dagster run config file for dev
- add constants file.

### Fix

- update checkIfTemplate
- add dagster home and fix python command.
- add commands to specify module to run.
- job config.
- set correct dagster-webserverversion.
- group on dep assets.
- remove unnecassary translator and made dlt_assets more common

## v0.10.0 (2024-07-18)

### Feat

- **pre-commit-config**: Add githook to prevent committing to main
- **setup.sh**: reverse change in setup.h and change to commitizen

## v0.9.0 (2024-07-10)

### Feat

- **ci**: Use commitizen to bump
- **ci**: add bump with commitizen
- **meta**: add commitizen configs to pyproject.toml
- **setup.sh**: reverse change in setup.h and change to commitizen

### Fix

- **ci**: create the new tag and add it in docker
- **ci**: check tags
- **ci**: change version tag setting from poetry to Git
- **ci**: check if version tag comes from poetry
- **ci**: add tag debug
- **docker-gh-action**: switch hack for commitizen

## v0.8.0 (2024-07-05)

## v0.7.0 (2024-07-04)

### Feat

- **setupsh**: add setup script
- **pre-commit-config**: Add pre-commit in pyproject, add pre-commit-config.yaml and add command for running pre-commit

### Fix

- **setup**: change command in setup
- **readme**: update install instructions
- **snowflake**: remove warehouse and role from necessarry config
- linting
- add ruff configuration
- move env.example to setup script

## v0.6.0 (2024-07-03)

### Feat

- **pyproject.toml**: Moved ipython and commitizen from depencies to dev.dependencies and removed prompt-toolkit

## v0.5.0 (2024-07-02)

## v0.4.0 (2024-07-02)

## v0.3.0 (2024-07-02)

## v0.2.0 (2024-07-02)

### Fix

- **docker**: fix broken reference to the dagsterproject
- add credentials to string

## v0.1.0 (2024-06-26)
