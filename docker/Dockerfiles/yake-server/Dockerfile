FROM library/python:3.7-alpine
RUN echo -e http://mirrors.ustc.edu.cn/alpine/v3.7/main/ > /etc/apk/repositories

# change to temp dir
WORKDIR /temp

RUN pwd
RUN pwd

# install git and build-base (GCC, etc.)
RUN apk update && apk upgrade && \
    apk add readline --repository=http://mirrors.ustc.edu.cn/alpine/v3.7/main && \
    apk add --no-cache bash git openssh && \
    apk add build-base

RUN pip install flasgger

# install requirements first to engage docker cache
RUN wget https://raw.githubusercontent.com/LIAAD/yake/master/requirements.txt -O requirements.txt
RUN pip install -r requirements.txt

# install yake via pip
#RUN pip install git+https://github.com/liaad/yake.git
RUN pip install git+https://github.com/Crazy-LittleBoy/yake.git

# Copy server startup script
COPY ./yake-rest-api.py /temp

# Expose server port
ENV SERVER_PORT 5000
EXPOSE "$SERVER_PORT"

# set default command
CMD [ "python", "yake-rest-api.py" ]
