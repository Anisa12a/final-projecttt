# Use an official Python runtime as a parent image
FROM python:3.12.0

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt

COPY . . 

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]