FROM library/python:3.11-alpine

# 换为国内源
#RUN echo -e http://mirrors.tuna.tsinghua.edu.cn/alpine/v3.17/main/ > /etc/apk/repositories
RUN echo -e http://mirrors.aliyun.com/alpine/v3.17/main/ > /etc/apk/repositories
RUN pip config set global.index-url http://mirrors.cloud.tencent.com/pypi/simple
RUN pip config set global.trusted-host mirrors.cloud.tencent.com

# change to temp dir
WORKDIR /temp

# install git and build-base (GCC, etc.)
RUN apk update && apk upgrade && \
    apk add --no-cache bash git openssh && \
    apk add build-base

# install yake via pip
RUN python -m pip install --upgrade pip
RUN pip install git+https://github.moeyy.xyz/https://github.com/python-greenlet/greenlet.git
#RUN pip install git+https://github.com/liaad/yake.git
RUN pip install git+https://github.moeyy.xyz/https://github.com/Crazy-LittleBoy/yake.git

# set default command
ENTRYPOINT ["yake"]
