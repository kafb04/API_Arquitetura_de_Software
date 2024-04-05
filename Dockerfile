FROM python
RUN apt-get update && apt-get install python3-pip -y
WORKDIR /projeto_asa
COPY projeto_asa /projeto_asa/
RUN pip install -r requirements.txt 
CMD ["uvicorn","main:app", "--host", "0.0.0.0", "--port", "8000"] 
