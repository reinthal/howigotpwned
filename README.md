# Datadrivet Loader Repo

TODO

- [ ] add flares with automation like  `datadrivet-infra-opendatastack` has ie [![CoCreate CI](https://github.com/knowit-solutions-cocreate/datadrivet-infra-opendatastack/actions/workflows/ci.yml/badge.svg)](https://github.com/knowit-solutions-cocreate/datadrivet-infra-opendatastack/actions/workflows/ci.yml)
- [ ] add tech stack diagram
- [ ] add CI
- [ ] Add commit hook to protect commit to main branch
- [x] Add commitizen to poetry.toml
- [x] Add commit hook to verify conventional commit format is adhered to
 

This is a template repo for setting up extract and load datapipelines for the [Datadrivet.ai Dataplatform](https://dagster.platform.datadrivet.ai).

## Purpose

To provide a Extract / Load starter-kit. Transformations and final tables are provided by a different repo TO BE DECIDED. 

Solutions Cocreate provides dataplatform-as-a-service so that developers can get data into our collective data warehouse fast.

If you use this repo you will get:

- A quickstart to get data from source systems into the raw database in Snowflake data warehouse

## Steps to Deploy

- [ ] Get access to Snowflake by emailing `alexander.reinthal at knowit dot se`
- [ ] Fork this repo
- [ ] Write your code to extract data using DLT
- [ ] Setup meeting with the Datadrivet Maintainers and do a handover. They will setup CI / CD using code developed in the forked repo.

## Prerequisites 

- git
- poetry
- python 3.10, 3.11 or 3.12
- docker for testing `docker build` (optional)
## How to install development environment (nix)

Without `direnv`

```

echo "Enter Snowflake database:"
read DATABASE
echo "Enter Snowflake username:"
read SNOWFLAKE_USERNAME
echo "Enter Snowflake password:"
read -s PASSWORD
cat << EOF > .envrc
use flake --experimental-features 'nix-command flakes'
watch_file ./nix/*
export DAGSTER_HOME=$(git rev-parse --show-toplevel)/dagster_project/dagster_home
export DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE=$DATABASE
export DESTINATION__SNOWFLAKE__CREDENTIALS__HOST="ut63892.north-europe.azure"
export DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME=$SNOWFLAKE_USERNAME
export DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD="$PASSWORD"
EOF
unset PASSWORD

```

and

```
nix develop
```

with `direnv

```
direnv allow
```

and then the environment should automatically build
## How to install development environment

Run this command to configure Snowflake credentials and install dependencies using poetry: 

```bash
 chmod +x setup.sh && ./setup.sh
```


## How run dagster

```bash
poetry run dagster dev
```

## How to run DLT

See `data_sources/README.md`

