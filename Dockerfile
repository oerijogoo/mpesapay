# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the Django project code to the container
COPY . .

# Expose the port on which your Django app will run (usually 7903)
EXPOSE 7903

# Define the command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:7903"]