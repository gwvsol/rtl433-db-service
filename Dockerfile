FROM python:3.11-bookworm
LABEL maintainer="Mikhail Fedorov" email="jwvsol@yandex.ru"
# LABEL stage=builder

ARG USER_ID
ENV USER_ID ${USER_ID:-1000}
ARG GROUP_ID
ENV GROUP_ID ${GROUP_ID:-1000}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN set -eux \
    && apt-get update \
    && apt-get install rtl-433 -y \
    && apt-get clean \
    && rm -rf /root/.cache/pip

ENV APP_DIR=/src
ENV APPS=rtl433db
ENV PATH=${PATH}:${APP_DIR}
COPY release/${APPS}-*.tar.gz /tmp/

RUN set -eux \
    && mkdir ${APP_DIR} \
    && mv /tmp/${APPS}-*.tar.gz ${APP_DIR} \
    && cd ${APP_DIR} \
    && tar -xvzf ${APPS}-*.tar.gz \
    && rm -fr *.tar.gz *.md *.yml Dockerfile

WORKDIR $APP_DIR

RUN make install-rtl433db \
    && make clean \
    && rm -fr .env archive \
        release $HOME/.cache/pip

ENTRYPOINT ["rtl433db-apps"]
