FROM python:3.10
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy all source code over
COPY . .

# Expose port 8000
EXPOSE 8000