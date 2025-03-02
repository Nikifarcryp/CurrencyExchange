# Step-by-Step Tutorial to Set Up and Launch the App
Step 1: Clone the Repository
First, clone the repository to your local machine using the following command:
git clone <repository_url>
cd <repository_name>

Step 2: Create a Virtual Environment
Create a virtual environment to manage your dependencies:
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Step 3: Install Dependencies
Install the required dependencies listed in the requirements.txt file:
pip install -r requirements.txt

Step 4: Set Up Environment Variables
Create a .env file in the root directory of your project and add the necessary environment variables:
alembic upgrade head

Step 5: Create a profile and obtain APILAYER API here https://apilayer.com/marketplace/currency_data-api .
It is entirely free.

Example of .env file:

SECRET_KEY="dhn4ouigj54605jfirevubhityohjrt"
ALGORITHM=HS256
SQLALCHEMY_DATABASE_URL='postgresql+asyncpg://{username}:{password}@{host}:{port}/{table_name}'
API_APILAYER=4983jrcv4gk9ceugjhtirfod
GMAIL_LOGIN=name@gmail.com
GMAIL_PASSWORD=xwebbzmiavlqapzz

Step 6: Run command (after docker installation)
docker compose -f docker-compose.yml up
Do this for appropriate work of Kafka

Step 7: Run Kafka Consumer
Open new terminal in parallel with a terminal where app is launched
Run command (being in route project repository): python3 app/kafka/email_consumer.py



Step 6: Run the Application
Start the FastAPI application using Uvicorn:
uvicorn app.main:app --reload

Step 7: Access the Application
Open your web browser and go to http://127.0.0.1:8000 to access the application. You can also access the automatically generated API documentation at http://127.0.0.1:8000/docs.
