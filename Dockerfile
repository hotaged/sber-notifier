FROM snakepacker/python:all as builder

RUN python3.10 -m venv /usr/share/python3/app \
     && /usr/share/python3/app/bin/pip install -U pip

COPY . .

RUN /usr/share/python3/app/bin/pip install -Ur requirements.txt \
    && python3.10 setup.py sdist \
    && /usr/share/python3/app/bin/pip install /dist/* \
    && /usr/share/python3/app/bin/pip check

FROM snakepacker/python:3.10 as api

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/* /usr/local/bin/

COPY pyproject.toml /usr/local/bin/
ADD migrations /usr/local/bin/migrations
WORKDIR /usr/local/bin/
