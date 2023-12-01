FROM python:3.9

WORKDIR /app

# Erstellen einer virtuellen Umgebung und Aktivierung
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "langchain_agent.py"]
