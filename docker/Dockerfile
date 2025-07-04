# Use official Python image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY src/ ./src/

# set environment
ENV PYTHONPATH=/app/src
CMD ["uvicorn", "tickethub.main:app", "--host", "0.0.0.0", "--port", "8000"]
