# Define base image
FROM continuumio/miniconda3
 
# Set working directory for the project
ENV MAIN_DIRECTORY /usr/src/app
ENV CODE_DIRECTORY /service

WORKDIR $MAIN_DIRECTORY

# Create Conda environment from the YAML file
COPY env.yml .
RUN conda env create -f env.yml

ENV PATH /opt/conda/envs/lab5_env/bin:$PATH

# Common file
COPY Logging.py .