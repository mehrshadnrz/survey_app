# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --system --deploy

# Copy the rest of the application code
COPY . .

RUN prisma generate

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
