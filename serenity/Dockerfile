# Use the official Python image from the Docker Hub
FROM python:3.11.5

# Set the working directory in the container
WORKDIR /serenity

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file into the container at /serenity
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
