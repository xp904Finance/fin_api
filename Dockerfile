FROM 49.234.85.212:5000/ubuntu-dev
MAINTAINER Finance https://github.com//orgs/xp904Finance/teams/jr-1904
WORKDIR /usr/src
ADD . /usr/src/Finance
WORKDIR /usr/src/Finance
VOLUME /usr/src/Finance
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
RUN pip install gunicorn -i http://mirros.aliyun.com/pypi/simple
RUN chmod +x run.sh
CMD /usr/src/Finance/run.sh