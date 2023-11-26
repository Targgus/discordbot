# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-bullseye

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG DISCORD_TOKEN
ARG GOOGLE_API_KEY

ENV DISCORD_TOKEN $DISCORD_TOKEN
ENV GOOGLE_API_KEY $GOOGLE_API_KEY

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade setuptools
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "app.py"]
