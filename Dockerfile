FROM python:3.10.12
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /ASA_TF
COPY . /ASA_TF/.
RUN pip install --upgrade pip
RUN pip install -r /ASA_TF/requirements.txt
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 