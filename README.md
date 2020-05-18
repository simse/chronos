<p align="center">
  <img alt="Chronos Logo" src="https://i.imgur.com/MoAbdWn.png" width="100" />
</p>
<h1 align="center">
  Chronos
</h1>
<p align="center">
A small Docker container to run and schedule Python 3.7 scripts
</p>

[![Build Status](https://travis-ci.com/simse/chronos.svg?branch=master)](https://travis-ci.com/simse/chronos)

## About
This container is good if you need to run a few or many Python scripts regularly, on a schedule or in response to certain events. The container runs Python 3.7 and thus is the interpreter used. Each script will be run in a virtual environment and it DOES support Pip dependencies. If you have access to the config directory, you can also run scripts and small modules bigger than one Python file.

In fact, if you're a bit handy, you can run anything you'd like, since the program simply calls an `execute.sh` file. In the future, I plan to add support for more scripting languages.

## Installation
This program is ONLY available as a Docker container. See section about security for more information.
```
docker pull simsemand/chronos
```
And then run:
```
docker run -p 5000:5000 -v CONFIG_PATH:/chronos simsemand/chronos
```

## Security
This program will run any script that is given to it. It will also accept any script sent to it via the REST API. Therefore, you should always, always, always run the program in the Docker container, as the scripts are NOT sandboxed on execution. You should also think very carefully about mounting any volumes to the container (except the config directory, of course), and if you do, consider putting it in read-only mode. As a final note, you should never expose Chronos to the public internet, unless you are using a reverse-proxy with proper authentication.

## Usage
- Add a new script by pressing the 'Add new' button
- Give it a name, you can always change the display name later
- This will take a short while, because it's creating a virtualenv
- Type in requirements in the proper Pip format
- Make sure to press the 'Install Pip requirements' button, they are not installed automatically
- Type in your script
- Choose an interval time (0 means never)
- Press save. The button should appear at the top of the screen at all times.

## Screenshots
You can find screenshots [right here](https://imgur.com/a/NJVumLw). Please bear in mind, this is dummy early beta.

## Bug reporting
If you found a bug, which wouldn't surprise me, please do send me an email at bug-reports@simse.io or better yet, open an issue on GitHub.
