# URL-Container
To quick start with docker:

   1. Clone this repository:
       ```bash
      git clone https://github.com/karina-kavaleuskaya/URL.git
      ```
    
   2. Build and start docker container
         ```bash
         docker-compose up --build
         ```
Default superuser will have email admin@mail.ru and password 12311
   

Without docker:
  1. Create database with name **url**
  2. Go to the project folder
       ```bash
        cd url_container
        ```
  3. Apply migrations
      ```bash
       python manage.py makemigrations
       python manage.py migrate
      ```
  4. Create superuser
     ```bash
       python manage.py createsuperuser
      ```
  5. Run the app
      ```bash
      python manage.py runserver
      ```
     

You can test this app with postman requests collection (it is in **_/test-project_** folder)
