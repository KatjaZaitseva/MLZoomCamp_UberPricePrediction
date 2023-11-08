# Uber Price Prediction for MLZoomCamp course

**Business objective**: Let's imagine we are working in Uber - the taxi company where the user may open the app and order a taxi service from different locations around the city. First, the user allows to detect his location, as the next step he chooses the location where he wants to get. Just with these variables, the app should return to the user a price which will help him to make the final decision - to make an order or not. Here comes the vital problem for the app - to show the price which will not scare off the user and at the same allow the business to remain profitable. Even though, for the customer, it may seem that the price is defined only by the distance, we may consider different factors - what is the weather at the moment of the request, what is the saturation level of the city, which cab was ordered, was it Business class or will the user travel with a pet or not. The goal of this project will be to **predict the price for the taxi with parameters which go beyond the distance**.

**Current solution:** Let's also imagine that right now, Uber has a simple model for predicting price with just one parameter - distance. This model will represent our baseline model.

**Main use case:** The output of the model will be used in the app to show customers the price for the ride that they requested.

---

## Table of Contents

- [Data](#data)
- [Machine Learning Model](#machine-learning-model)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Deployment](#deployment)

## Data

The dataset used for training the machine learning model can be found on Kaggle: [Uber and Lyft Dataset Boston, MA](https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma/data). Since the dataset is 367.38 MB, to reproduce the code, it is needed to install the dataset locally and put it into the folder `/inputs`

## Machine Learning Model

After considering various models, it was decided on the Gradient Busting model developed with XGBRegressor. This model is used to predict the price (continuous variable) taking into account other available parameters when requested by the user.

## Dependencies

This project uses `pipenv` for managing the Python environment and dependencies. Ensure you have the following installed:

- Python (version 3.9)
- `pipenv` (Python package for managing virtual environments)

## Installation

### Step 1: Python and Git

If not already installed, download and install Python from [Python's official website](https://www.python.org/).
Additionally, you'll need Git to clone the repository. Install Git from [Git's official website](https://git-scm.com/) if not already present.

### Step 2: Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction.git
cd MLZoomCamp_UberPricePrediction
```

### Step 3: Download the data

Go to the [Uber and Lyft Dataset Boston, MA](https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma/data) on Kaggle and click `Download` button near the dataset:

<img width="1055" alt="image" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/c46fb9fa-44d2-481c-b2a5-3ff7fc291411">

After successful loading, put the file inside the folder `MLZoomCamp_UberPricePrediction/inputs`. You can move the `rideshare_kaggle.csv` file to the `MLZoomCamp_UberPricePrediction/inputs` directory using the `mv` command in the terminal. Here's how you can do it:

1. **Open your terminal**.

2. **Navigate to the directory where you downloaded the file**. If the file was downloaded to your default "Downloads" directory, you would do something like this:

   ```sh
   cd ~/Downloads
   ```

   *(Note: The tilde `~` symbol represents your home directory. If your file is in another directory, replace `~/Downloads` with the actual path where your file is located.)*

3. **Use the `mv` command to move the file**. Execute the following command:

   ```sh
   mv rideshare_kaggle.csv /path/to/your/MLZoomCamp_UberPricePrediction/inputs/
   ```

   Replace `/path/to/your/` with the actual path where your `MLZoomCamp_UberPricePrediction` directory is located. If you are currently in your home directory and `MLZoomCamp_UberPricePrediction` is also directly under your home directory, it would look like this:

   ```sh
   mv rideshare_kaggle.csv ~/MLZoomCamp_UberPricePrediction/inputs/
   ```

   Make sure the `inputs` directory already exists inside `MLZoomCamp_UberPricePrediction`. If it does not, you can create it using:

   ```sh
   mkdir -p ~/MLZoomCamp_UberPricePrediction/inputs
   ```

4. **Check to ensure the file was moved**. Navigate to the `inputs` directory and list the files to confirm the `rideshare_kaggle.csv` file was successfully moved:

   ```sh
   cd ~/MLZoomCamp_UberPricePrediction/inputs
   ls
   ```

   You should see `rideshare_kaggle.csv` listed there.

Remember to replace `~/MLZoomCamp_UberPricePrediction/inputs/` with the correct path if your `MLZoomCamp_UberPricePrediction` directory is located somewhere other than your home directory.

### Step 4: Set Up the Environment

Ensure `pipenv` is installed. If not, install it via pip:

```bash
pip install pipenv
```

Then, create the virtual environment and install dependencies using `pipenv`:

```bash
pipenv install
```

### Step 4: Activate the Environment

Activate the virtual environment to work within it:

```bash
pipenv shell
```

### Step 5: Training the model

Once the environment is activated, you should be able to train the model by running:

```bash
python train.py
```

This will create the model and save it in the folder. However, it's also possible to play with a notebook by running a command:

```bash
jupyter notebook
```

This will open `http://localhost:8888/tree` where you can open the notebook and look at the EDA analysis, dataset itself and model selection approach.

## Deployment

The machine learning model has been deployed as a web service using Flask and Docker.

### Local Deployment with Docker

The model is loaded and put inside a web service called `price_prediction` using Flask (see `predict.py`). This service is then put inside a python virtual environment pipenv. To recreate this environment Pipfile and Pipfile.lock is provided. To be able to run the app `price_prediction` on any computer, we put it inside a docker container (see `Dockerfile`).

1. **Build the Docker Image:**
   - Use the following command to build the Docker image:

   ```bash
   docker build -t uber-price-prediction .
   ```

2. **Run the Docker Container:**
   - Start a container locally using the following command:

   ```bash
   docker run -it -p 9696:9696 uber-price-prediction:latest
   ```

3. **Access the Application:**
   - Double-check the `url` variable in the `test.py` script located in the `testing` folder so that the port matches with the one that we used to run the docker container: `http://localhost:9696/predict`. After making all changes, execute the `test.py` script. This will enable you to view the response in JSON format, displaying the predicted price for the requested ride.

### Deployment to AWS Elastic Beanstalk using `awsebcli`

As the final step, we deploy our docker container built in the previous step to the cloud.

1. **AWS Account and Access Keys:**
   - Ensure you have an active AWS account before deploying to Elastic Beanstalk using `awsebcli`. You can follow the instructions on how to create the account in AWS in [this article](https://mlbookcamp.com/article/aws)
   - You'll need the Access Key ID and Secret Access Key associated with your AWS account to configure `awsebcli`. To find it, go to Identity and Access Management (IAM) in AWS -> Users -> NameOfCreatedUser -> Security credentials -> Create access keys. These Access Keys are used for authentication to AWS services.
  
2. **Install and Configure `awsebcli` in your virtual environment:**
   - Install `awsebcli` by running:
   ```bash
   pipenv install awsebcli --dev
   ```
   - Configure `awsebcli` by running:
   ```bash
   eb init -p docker -r eu-west-3 price-prediction-serving
   ```
   - By the command `-p` you can specify which platform you want to use (e.g. for the current project docker was replaced with `Docker running on 64bit Amazon Linux 2` due to the [bug about Generic Docker](https://github.com/awsdocs/aws-elastic-beanstalk-developer-guide/issues/149#issue-1634369387))
   - By the command `-r` you can specify the region. I used `eu-west-3` but Alexey said that `eu-west-1` is cheaper (:
   - `price-prediction-serving` - name of the Elastic Beanstalk

3. **Test locally**
   - Before we deploy our Dockerized application, we can test it locally by running:
   ```bash
   eb local run --port 9696
   ```
   - Replace 9696 with your port
   - Open a new terminal and run
   ```bash
   python test.py
   ```

4. **Deploy to Elastic Beanstalk:**
   - Deploy Dockerized application to Elastic Beanstalk by executing the following command:
   ```bash
   eb create myapp-env
   ```
   - Replace myapp-env with your desired environment name. For this project, we used the name `price-prediction-serving-env`

5. **Access the Application:**
   - After creating the env (which may take some time), we need to copy the link from the row 'Application available at' and update the `url` variable in the `test-aws.py` script. Now, we are using AWS host instead of localhost. After making this change, execute the `test-aws.py` script. This will enable you to view the response in JSON format running on AWS service.

The outcomes of the deployment:
<img width="874" alt="Screenshot 2023-11-08 at 21 29 38" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/33c88c2e-c2ce-403c-9f7f-3a52ec102a3c">
<img width="761" alt="image" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/ac48d09b-5642-4bb2-86d4-73c3a67306f8">
<img width="980" alt="image" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/cfab9bf4-12ec-4bde-b8ca-54c4de2564dc">

6. **Terminate the environment:**

```bash
eb terminate myapp-env
```
<img width="867" alt="image" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/b9392366-432d-47a7-a1ab-a26935601221">

<img width="1047" alt="image" src="https://github.com/KatjaZaitseva/MLZoomCamp_UberPricePrediction/assets/37984099/ab7e86f0-dbf5-4960-bbe2-be18afd0eafe">


