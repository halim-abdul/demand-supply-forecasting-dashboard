FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt && pip install -e .
COPY . .
EXPOSE 8000 8501
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
