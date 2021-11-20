FROM python:3.7-buster
LABEL author="Simon Sorensen (hello@simse.io)"

# Set timezone to Greenwich Mean Time
ENV TZ=GMT
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install node
RUN curl -sL https://deb.nodesource.com/setup_16.x -o nodesource_setup.sh && \
    bash nodesource_setup.sh && \
    apt-get update && \
    apt-get install -y nodejs && \
    rm nodesource_setup.sh && \
    apt-get clean && \
    npm install -g yarn

# Install common packages
RUN apt-get update
RUN pip install cython
RUN apt-get install -y freetds-dev
RUN pip install pymssql

# Copy Chronos to image
COPY . /app/chronos

# Build Chronos UI
WORKDIR /app/chronos/chronos-ui
RUN yarn
RUN yarn build

# Set enviroment and expose ports and directories
EXPOSE 5000
VOLUME /chronos
ENV CHRONOS_PATH=/chronos
ENV CHRONOS=yes_sir_docker

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

# Install Python dependencies
WORKDIR /app/chronos
RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "app.py"]
