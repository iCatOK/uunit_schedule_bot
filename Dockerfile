FROM python:3.11.1-alpine3.16

# Locale
ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl
ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
    && unzip musl-locales-master.zip \
      && cd musl-locales-master \
      && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
      && cd .. && rm -r musl-locales-master

WORKDIR /bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app ./app
COPY poetry.lock pyproject.toml ./

RUN python3 -m pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry env use system && poetry install

ENV PYTHONPATH "${PYTHONPATH}:/bot/app/"

CMD ["python3", "/bot/app/main.py"]