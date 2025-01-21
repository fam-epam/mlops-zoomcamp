FROM python:3.10-slim

RUN pip install mlflow==2.12.1

EXPOSE 8080

CMD [ \
    "mlflow", "server", \
    "--backend-store-uri", "sqlite:///home/mlflow_data/mlflow.db", \
    "--host", "0.0.0.0", \
    "--port", "8080" \
]