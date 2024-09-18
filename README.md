# Sample Assignment


### How to setup locally
#### Requirements

- Python3
- pip
- venv


#### setup instructions

- create   a virtualenv using venv
```cmd
   python -m pip install --upgrade pip
   python3 -m venv venv
   ```
- activate it 
```cmd
   source venv/bin/activate
   ```
- or activate Windows
```cmd
   venv/bin/activate.bat
   ```
- install dependencies from the requirements.txt file
```cmd
   pip install -r requirements.txt
   ```
- connect to postgresql database
```cmd
   create psql database with name catalyst_count and connect according to django settings
   ```

- migrate the database tables
```cmd
   python manage.py migrate
   ```
- create a new superuser
```cmd
   python manage.py createsuperuser
   ```
- start a development server using 
```cmd
   python manage.py runserver
   ```

- start a postman application and export the api collection
```cmd
   check the UI
   ```

FYI - 
  Test cases are not included.
  Forgot Password is not implemented.
  UI is not as per design images.







