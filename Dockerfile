FROM python:3.9

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get -y install coinor-cbc  # install CBC solver (untested)

RUN pip install pip-tools

RUN pip-compile

RUN pip-sync

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]
