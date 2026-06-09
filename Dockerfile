FROM python:3.9-slim

# Copy the AWS Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# We copy the app directory specifically to match the app.main import
COPY app/ ./app/

# The Lambda Web Adapter requires the port to be 8080 by default
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Command to run the application (Updated for Lambda)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
