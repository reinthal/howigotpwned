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
