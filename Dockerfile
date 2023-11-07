FROM python:3.9-slim-buster

# Install pipenv library in Docker 
RUN pip install pipenv

# create a directory in Docker named app and we're using it as work directory 
WORKDIR /app  
# Copy the Pip files into our working derectory 
COPY ["Pipfile", "Pipfile.lock", "./"]

# install the pipenv dependencies for the project and deploy them.
#The flags --deploy and --system makes sure that we install the 
#dependencies directly inside the Docker container without 
#creating an additional virtual environment
RUN pipenv install --system --deploy

# Copy any python files and the model we had to the working directory of Docker 
COPY ["*.py", "price_prediction.bin", "./"]

# We need to expose the 9696 port because we're not able to communicate with Docker outside it
EXPOSE 9696

#Run it with Gunicorn
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "predict:app"]