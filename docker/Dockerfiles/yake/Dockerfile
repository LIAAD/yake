FROM library/python:3.7.1-alpine

# change to temp dir
WORKDIR /temp

# install git and build-base (GCC, etc.)
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

# install yake via pip
RUN pip install git+https://github.com/liaad/yake.git

# set default command
ENTRYPOINT ["yake"]
