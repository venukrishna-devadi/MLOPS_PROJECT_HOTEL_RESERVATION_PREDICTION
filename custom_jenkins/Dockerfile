### This Docker file is for JENKINS CONTAINER

# Use the official Jenkins LTS image
FROM jenkins/jenkins:lts

# Switch to root user to install Docker
USER root

# Install Docker using the official convenience script
RUN apt-get update && \
    apt-get install -y curl sudo && \
    curl -fsSL https://get.docker.com | sh

# Add Jenkins user to Docker group
RUN usermod -aG docker jenkins

# Optional: create the Docker volume directory if you plan to mount it
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins