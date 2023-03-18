# Define base image
FROM lab5-base-image
 
# Set working directory for the project
WORKDIR $MAIN_DIRECTORY
 
# Python program to run in the container
COPY *.py $MAIN_DIRECTORY$CODE_DIRECTORY/

EXPOSE 10000

ENTRYPOINT ["python", "service/main.py", "-p", "10000"]
