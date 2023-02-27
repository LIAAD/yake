FROM library/python:3.7-alpine
RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.7/main/ > /etc/apk/repositories

# change to temp dir
WORKDIR /temp

# install git and build-base (GCC, etc.)
RUN apk update && apk upgrade && \
    apk add readline --repository=http://mirrors.ustc.edu.cn/alpine/v3.7/main && \
    apk add --no-cache bash git openssh && \
    apk add build-base

# install yake via pip
#RUN pip install git+https://github.com/liaad/yake.git
RUN pip install git+https://github.com/Crazy-LittleBoy/yake.git

# set default command
ENTRYPOINT ["yake"]
