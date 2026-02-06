FROM python:3.10-slim

WORKDIR /app

RUN apt-get update

# At first we should to copy requirenments.txt, and install dependencies
COPY ./streamlit_service/requirements.txt /app
RUN pip3 install -r requirements.txt

COPY ./streamlit_service/* /app

# Opening outside port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
