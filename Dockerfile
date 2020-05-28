FROM python:3.7-buster
LABEL author="Simon Sorensen (hello@simse.io)"

# Set timezone to Greenwich Mean Time
ENV TZ=GMT
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Add yarn to apt
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

# Install common packages
RUN apt-get update
RUN pip install cython
RUN apt-get install -y freetds-dev
RUN pip install pymssql

# Install Node and Yarn
RUN apt-get install -y nodejs yarn

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

# Install Python dependencies
WORKDIR /app/chronos
RUN pip install -r requirements.txt

ENTRYPOINT python chronos.py
