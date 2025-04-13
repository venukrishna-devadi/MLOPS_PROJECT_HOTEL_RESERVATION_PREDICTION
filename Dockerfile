### THIS DOCKER FILE IS FOR PROJECT - TO DOCKERIZE WHOLE PROJECT

# slim -> lightweight image
FROM python:slim

# we dont want our environment to overwrite any files
# Prevents Python from writing .pyc files to disk. 
# This is useful in Docker containers where you might not want to persist these files

#PYTHONUNBUFFERED=1: Disables buffering for Python's stdout and stderr streams. 
# This ensures that output is displayed immediately, which can be 
# helpful for logging and debugging purposes

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# set working directory
WORKDIR /app

# install some dependencies
RUN apt-get update && apt-get-install -y --no-install-recommends \

# installing light gbm dependecies
    libgomp1 \
    && apt-get-clean \
    && rm -rf /var/lib/apt/lists/*

# for copying all the code from the project directory
COPY . .

# we are just avoiding cache by not installing any cache
RUN pip install --no-cache-dir -e .

# train the model
RUN python pipeline/training_pipeline.py

# we want to expose the port
EXPOSE 5000

# to run the app
CMD ["python", "application.py"]



