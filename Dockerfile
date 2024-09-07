# Production stage
FROM python:3.12-slim

WORKDIR /python-docker

# Copy only the necessary files for production
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Create a new user with UID 10016
RUN addgroup -g 10016 choreo && \
    adduser  --disabled-password  --no-create-home --uid 10016 --ingroup choreo choreouser
USER 10016

EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
