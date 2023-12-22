# streamlit/Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# here we store the db's
ENV DATA_PATH /app/data/

ENTRYPOINT ["streamlit", "run", "streamlit_app4.py", "--server.port=8501", "--server.address=0.0.0.0"]