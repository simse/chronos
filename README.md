<p align="center">
  <img alt="Chronos Logo" src="https://github.com/simse/chronos/raw/master/logo.png" width="80" />
</p>
<h1 align="center">
  Chronos
</h1>
<p align="center">
A small Docker container to run and schedule Python scripts
</p>

[![Build Status](https://travis-ci.com/simse/chronos.svg?branch=master)](https://travis-ci.com/simse/chronos)

## About
Chronos is a simple application to execute Python scripts in response to certain events. Each script will be assigned a virtual environment and folder, allowing Pip dependencies to be installed with conflicting with other scripts. The current Python version is 3.7.

Chronos is not intended for larger Python scripts that are meant to run forever, or listen on ports (yet!).

## Installation
You may install Chronos via Docker.
```
docker pull simsemand/chronos
```
And then run:
```
docker run -p 5000:5000 -v CONFIG_PATH:/chronos simsemand/chronos
```

## Security
Please do not expose Chronos to the public internet. At the moment there is zero security against unauthorised access, and attackers *would* be able to execute malicious code on your server quite easily.

## Features
- Beautiful and functional web UI
- Fast and lightweight
- Ability to create individual virtual environments
- Interval triggers (e.g. every 10 seconds)
- CRON triggers (e.g. every 5th day of the month)
- `stdout` and `stderr` output capture
- Live script output capture (so you know it's still working)
- You can easily trigger a script using the api: http://[ChronosIp]:[ExposedPort]/api/script/[NameOfScript]/execute

## Feature requests
Trivial requests will usually be added quickly. Larger requests will take a little longer. I am, after all, still a busy university student.

## Screenshots
You can find screenshots [right here](https://imgur.com/a/PQdH5ro).

## Bug reporting
If you found a bug, which wouldn't surprise me, please do send me an email at bug-reports@simse.io or better yet, open an issue on GitHub.
