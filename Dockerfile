# syntax=docker/dockerfile:1

FROM python:3.12.9

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

COPY . .

RUN uv sync --frozen

EXPOSE 3100

CMD ["uv", "run", "main.py"]