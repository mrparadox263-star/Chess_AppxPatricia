# Start with a clean Linux environment
FROM python:3.11-slim

# Install C++ compilers, build tools, and Git
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    clang \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create our app workspace
WORKDIR /app

# Copy your web app files into the container
COPY . .

# Clone Patricia directly, compile it, and extract the engine and nets!
RUN git clone https://github.com/Adam-Kulju/Patricia.git /tmp/patricia && \
    cd /tmp/patricia/engine && \
    make -B CXXFLAGS="-O3 -std=c++20 -ffast-math -march=x86-64" && \
    cp patricia /app/patricia && \
    cp -r nets /app/

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Grant execution permissions to the new binary
RUN chmod +x patricia

# Start the web server
CMD gunicorn app:app --bind 0.0.0.0:$PORT
