"# files_Upload" 
## Installation Steps for Frontend
1. Clone the repository:
   ```bash
   git clone https://github.com/hubgitpoonam/FileUpload.git
   cd frontend

2. npm install

3. REACT_APP_API_URL = "your_backend url"

4. npm start


## Installation Steps for Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/hubgitpoonam/FileUpload.git
   cd fileupload

2. python -m virtualenv venv or virtualenv env

3. Activate the virtual environment:

        On Windows:
        venv\Scripts\activate      
       

4. pip install -r requirements.txt

5. create .env file in root directory of fileUpload
   .env

6. .env file should contain 
    # .env file

    # Database settings
    DB_NAME="your_db_name"
    DB_USER="your_user_name"
    DB_PASSWORD="your_password"
    DB_HOST="hostname"
    DB_PORT="port_number"

    # CORS Origin
    CORS_ORIGIN_WHITELIST="your frontend URl"


6. python manage.py migrate

8. python manage.py runserver
