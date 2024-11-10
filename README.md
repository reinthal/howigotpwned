[![Continuous Integration](https://github.com/reinthal/leakme/actions/workflows/ci.yaml/badge.svg)](https://github.com/reinthal/leakme/actions/workflows/ci.yaml)
[![Continuous Delivery](https://github.com/reinthal/leakme/actions/workflows/cd.yaml/badge.svg)](https://github.com/reinthal/leakme/actions/workflows/cd.yaml)

```
.__                      .___   ________           __   __________                              .___
|  |__    ____  __  _  __|   | /  _____/   ____  _/  |_ \______   \__  _  __  ____    ____    __| _/
|  |  \  /  _ \ \ \/ \/ /|   |/   \  ___  /  _ \ \   __\ |     ___/\ \/ \/ / /    \ _/ __ \  / __ |
|   Y  \(  <_> ) \     / |   |\    \_\  \(  <_> ) |  |   |    |     \     / |   |  \  ___/ / /_/ |
|___|  / \____/   \/\_/  |___| \______  / \____/  |__|   |____|      \/\_/  |___|  / \___  >\____ |
     \/                               \/                                         \/      \/      \/
```

# howigotpwned

How I got pwned? What website exactly leaked my credentials and what password did I use? Thats the goal of this project

## How did the project start?

I was looking up myself in [Have I been pwned](https://haveibeenpwned.com/), a website dedicated to tracking leak data, and I found recent dump named Cit0day which allagedly had my email and cleartext password. I am guilty of some historical password reuse, so I was of course very interested in what password I needed to change as changing all 100+ passwords is way too much work for some 1-off throw away account I used gmail for.

## Milestones

- [x] add concurrency limits
- [ ] Minio/Nessie garbage collection AWS_REGION
- [ ] Make a search frontend
- [ ] Add spark/pyspark
- [x] Add domain column for `int_passwords` asset
- [x] Add categorical for type of password for `int_password`
- [x] Re-partition passwords
- [x] configure nessie branch
- [x] unrar rar files
- [x] find format of 1 file
- [x] generalize
- [x] setup sops for repo
- [x] rewrite dagster pipelines for pre-extracted data
- [x] setup dagster job
- [x] deploy to prod

# Version pins

- [ ] Pinned pyiceberg, waiting for release 0.8.0

# Chores

- [x] fix utf-8 encoding issue

## How to install development environment (nix)

and
with `direnv

```
direnv allow
```

and then the environment should automatically build
