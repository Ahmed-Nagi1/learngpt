# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
   && apt-get install -y binutils libproj-dev gdal-bin gettext-base gettext \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /learn

# Install Python dependencies
COPY requirements.txt /learn/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /learn/
COPY . /learn/

# Copy entrypoint script into container
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint.sh executable
RUN chmod +x /entrypoint.sh

# Run entrypoint.sh script when the container starts
ENTRYPOINT ["/entrypoint.sh"]
