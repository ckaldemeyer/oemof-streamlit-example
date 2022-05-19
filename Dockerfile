FROM python:3.7

WORKDIR /app

COPY . /app

RUN ls -l

RUN pip install pip-tools

RUN pip-compile

RUN pip-sync

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]