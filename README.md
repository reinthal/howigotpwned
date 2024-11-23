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
## Ethical Considerations User Notice 

### Introduction 

Welcome to howigotpwned GitHub repository, which provides tools designed to index and search publicly leaked passwords. While this tool can serve numerous legal and educational purposes—such as allowing security researchers to study data breaches, or assisting in password strength awareness — it is critically important that these tools be used responsibly and ethically. 

### Notice of Ethical Use 

By using the software, data, and associated documentation available in this repository, you agree to adhere to the ethical considerations as outlined here and respect all applicable laws and regulations. Your intention in using this software should be to promote better security practices, raise awareness, or contribute positively to technological and educational advancements, and not to engage in or promote malicious activities. 

### Discoraged Usages 

Using this code to: 

    Engage in Unauthorized Access: 
    Using information contained within this repository to attempt gaining unauthorized access to any accounts, systems, or networks is illegal and against the terms of use for this project. 

    Harm Individuals: 
    Applying this tool to harass, harm, or infringe upon the privacy or security of individuals is unacceptable. This includes, but is not limited to, using leaked data to partake in threats, identity theft, or personal attacks. 

    Sell Data: 
    Selling data indexed using this repository is a violation of the spirit of this project and potentially violates laws regarding the handling of personal data. 

    Promote Illicit Activities: 
    Distributing information from this repository or otherwise using it to encourage or facilitate criminal activities is strictly prohibited. 
     

### Expectations for Usage 

Users are expected to: 

    Intended Purpose: 
    Employ this tools only for purposes that are clearly ethical, such as security research, educational projects, or advancing the security of systems and applications. 

    Harm-prevention use: 
    Data indexed within this repository should be used for the purpose of resetting leaked passwords for you, the organisation you represent or peers that you care about.  


### Legal Compliance 

Compliance with all applicable laws and regulations is recommended when using any tool or data indexed from this repository. This includes but is not limited to data protection statutes and criminal codes. If you are unsure or have questions, seek legal counsel prior to engaging with this repository. 

### Conclusion 

This repository aims to contribute to the cybersecurity community by providing tools for educational, research, and security-enhancement purposes. We trust users to uphold the highest ethical standards in all usage of this software. Any deviation from these guidelines is strictly at the user's risk and may have legal consequences. 

Remember: With great power comes great responsibility. Use these tools wisely and ethically.  

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
