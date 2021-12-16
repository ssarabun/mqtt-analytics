# Python image to use.
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

EXPOSE 5000/tcp

ENV FLASK_APP=flaskr

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

RUN flask init-db

# Run app.py when the container launches
#ENTRYPOINT ["python", "app.py"]
CMD gunicorn --workers 1 --bind 0.0.0.0:5000 app:app
