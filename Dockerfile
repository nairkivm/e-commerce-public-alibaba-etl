# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for logs
RUN mkdir -p /usr/src/app/logs

# Copy the rest of the application code into the container
COPY . .

# Grant execute permission to your script
RUN chmod +x run_scripts.sh

# Command to run the ETL pipeline with arguments
CMD ["./run_scripts.sh"]
