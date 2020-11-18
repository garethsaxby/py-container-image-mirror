# py-container-image-mirror

This repository contains a simple Python utility designed to mirror container images from one registry to another.

## Requirements

- Tested on Python 3.9 currently
- A local Docker server API must be reachable

## Usage

### Basic Usage

```shell
pip install -r requirements.txt
python cim.py --help # Show options; run without --help to be prompted
```

### Provide Options Directly

```shell
python cim.py -r "registry.hub.docker.com/library/ubuntu" -t "20.04" -d "registry.hub.docker.com/user/repository" -T "latest" -u "username" -p "password"
```

## Further Updates

This is currently a first-run; see [TODO.md](TODO.md) for possible further improvements.

## Original Problem Statement

This tool was created due to the [Docker Rate Limiting](https://www.docker.com/blog/what-you-need-to-know-about-upcoming-docker-hub-rate-limiting/), effective as of November 2020.

Dockerhub has begun limiting container image pull rates over time, meaning that users may find themselves unable to pull container images if they have hit that limit.

Beyond paying for Dockerhub, for which paid accounts have no rate limits, it's generally best practice to keep your container images in a localised registry to maintain tight control over them and avoid repeated bandwidth costs from multiple pulls, as well as mitigating the afformentioned Dockerhub limit.

This utility fills that role, by pulling images once and mirroring them up to an alternative container registry of your choice; it can also be used to generally mirror images from any registry. not just Dockerhub.
