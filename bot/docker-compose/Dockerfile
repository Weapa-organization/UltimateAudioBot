FROM python:3.9 AS build

# Enable venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./bot/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -Ur ./requirements.txt

FROM python:3.9-slim

# date system Madrid
ENV TZ=Europe/Madrid
# environment
ENV ENVIRONMENT=develop
# bot token
ENV BOT_TOKEN=""
# bot name
ENV BOT_NAME=bot_name

# Copy venv from builder
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN apt update && apt install -y ffmpeg libavcodec-extra \
    libpulse0 libasound2 libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./bot/src ./

# COPY ./bot/docker-compose/entrypoint.sh ./entrypoint.sh
# RUN chmod +x ./entrypoint.sh


# ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "bot.py"]