FROM python:3.8 as requirements_stage

WORKDIR /wheel

RUN python -m pip install --user pipx

COPY ./pyproject.toml \
  ./requirements.txt \
  /wheel/


RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN python -m pip wheel --wheel-dir=/wheel --no-cache-dir --requirement ./requirements.txt

RUN python -m pipx run --no-cache nb-cli generate -f /tmp/bot.py


FROM python:3.8-slim

WORKDIR /app

ENV TZ Asia/Shanghai
ENV PYTHONPATH=/app

COPY --from=requirements_stage /tmp/bot.py /app

COPY --from=requirements_stage /wheel /wheel

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir --no-index --find-links=/wheel -r /wheel/requirements.txt && rm -rf /wheel 

COPY . /app/

CMD ["python", "bot.py"]