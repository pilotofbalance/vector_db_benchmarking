# Use a base image with your preferred Linux distribution and Python version
FROM python

# Install required dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libomp-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Faiss using pip
RUN pip install faiss-cpu
RUN pip install config atomicwrites attrs Click Flask intel-openmp itsdangerous Jinja2 more-itertools numpy pathlib2 pluggy py pytest pytest-flask six Werkzeug

# Set the working directory
WORKDIR /app

# Copy your Faiss code and data into the container
COPY . .

# Run your Faiss application
CMD ["python", "app.py"]