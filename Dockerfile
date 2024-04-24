FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /ASA_TF
COPY . ASA_TF
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 
