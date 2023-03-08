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

RUN python -m pip install --upgrade pip
RUN pip install flasgger

# install requirements first to engage docker cache
# RUN wget https://raw.githubusercontent.com/LIAAD/yake/master/requirements.txt -O requirements.txt
#RUN #pip install greenlet==0.4.5
#RUN pip install git+https://github.moeyy.xyz/https://github.com/python-greenlet/greenlet.git
#RUN pip install meinheld
#RUN pip install git+https://github.moeyy.xyz/https://github.com/mopemope/meinheld.git@1.0.2
RUN pip install git+https://github.moeyy.xyz/https://github.com/idot/meinheld.git@2bfe452d6608c92688d92337c87b1dd6448f4ccb
RUN wget https://raw.githubusercontent.com/Crazy-LittleBoy/yake/master/requirements.txt -O requirements.txt
RUN pip install -r requirements.txt

# install yake via pip
#RUN pip install git+https://github.com/liaad/yake.git
RUN pip install git+https://github.moeyy.xyz/https://github.com/Crazy-LittleBoy/yake.git

# Copy server startup script
COPY ./yake-rest-api.py /temp

# Expose server port
ENV SERVER_PORT 5000
EXPOSE "$SERVER_PORT"

# set default command
CMD [ "python", "yake-rest-api.py" ]
