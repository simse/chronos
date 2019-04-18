<p align="center">
  <img alt="Gatsby" src="https://i.imgur.com/MoAbdWn.png" width="60" />
</p>
<h1 align="center">
  Chronos
</h1>
<p align="center">
A small Docker container to run and schedule Python 3.7 scripts
</p>


## About
This container is good if you need to run a few or many Python scripts regularly, on a schedule or in response to certain events. The container runs Python 3.7.3 and thus is the interpreter used. Each script will be run in a virtual environment and it DOES support Pip dependencies. If you have access to the config directory, you can also run scripts and small modules bigger than one Python file.

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

More README to come.
