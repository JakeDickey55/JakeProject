#name: JakeCrypto
#syntax=docker/dockerfile:1
#check=skip=SecretsUsedInArgOrEnv

FROM alpine:latest

# Update apk repositories and install system dependencies
RUN apk update \
 && apk add \
 --no-cache \
    python3-dev \
    postgresql-dev \
    py3-aiohttp \
    py3-dotenv \
    py3-pip \
    py3-requests \
    py3-yaml \
    libpq-dev \
    gcc \
    libc-dev \
    make \
    curl \
    git \
    zip \
    curl \
    unzip

# Install Python dependencies using pip3
RUN pip3 install --break-system-packages \
    psycopg2-binary \
    fastapi \
    fastapi[standard] \
    uvicorn \
    pydantic \
    sqlalchemy \
    sqlalchemy-utils \
&& rm -rf /var/cache/apk/*
RUN git clone https://github.com/noxdafox/clipspy.git \
    && cd clipspy \
    && make && make install 
    
    # Lazy workaround to add clips to PATH variable
    ENV PATH="${PATH}:/clipspy/clips_source"

WORKDIR /app


# Copy application files
COPY . .

# Expose the application port
EXPOSE 8000

# Default command to run FastAPI app
CMD ["uvicorn", "API:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternate command for debugging
# CMD ["tail", "-f", "/dev/null"]
