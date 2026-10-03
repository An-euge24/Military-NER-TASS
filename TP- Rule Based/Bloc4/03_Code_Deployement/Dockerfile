FROM python:3.11-slim
WORKDIR /app
COPY Bloc4/02_Code_Developpement/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY Bloc4/02_Code_Developpement /app
COPY Bloc4/03_Code_Deployement/api.py /app/api.py
COPY model_ner /app/model_ner
ENV MODEL_PATH=/app/model_ner
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
