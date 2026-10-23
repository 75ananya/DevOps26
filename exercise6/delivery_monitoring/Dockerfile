FROM python:3.10-slim
WORKDIR /app
RUN pip install prometheus-client
COPY delivery_metrics.py .
CMD ["python", "-u", "delivery_metrics.py"]