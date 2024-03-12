# Use a base image with your preferred Linux distribution and Python version
FROM python

# Install required dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Chroma Db using pip
RUN pip install chromadb atomicwrites attrs Click Flask intel-openmp itsdangerous Jinja2 more-itertools numpy pathlib2 pluggy py pytest pytest-flask six Werkzeug

# Set the working directory
WORKDIR /app

# Copy your Chroma code and data into the container
COPY . .

USER root
RUN chmod +x ./start.sh

# CMD ["sh","./start.sh"]
CMD ["python", "app.py"]