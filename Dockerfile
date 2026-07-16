# Start with a clean Linux environment that has Python installed
FROM python:3.11-slim

# Install the necessary C++ compilers (including clang) and build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Create a workspace folder inside the container
WORKDIR /app

# Copy all your GitHub files (app.py, source code, .nnue files) into the container
COPY . .

# Compile the Patricia engine using generic x86-64 architecture
RUN make clean && make -B CXXFLAGS="-O3 -std=c++20 -ffast-math -march=x86-64"

# Install your Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Grant execution permissions to the newly built binary
RUN chmod +x patricia

# Start the Flask web server using Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:$PORT
