# GiveThingsBack
Website allowing people to clear out things, that they no longer need in home.  
The goal here is to make sure that trusted foundations will take care of your things and give them second life.  
You can check it by yourself at http://givethingsback.herokuapp.com/

### Automatic installation

Open terminal in repository directory.  
Run: ```chmod 777 ./install.sh```  
After that you can install script by ```./install.sh``` command in terminal (make sure you are in the same directory)

### Important
In ```GiveThingsBack/GiveThingsBack``` folder, update ```local_settings.py.txt```  to
your own settings and delete ```.txt``` from the end of a file.  
Please configure e-mail service at the end of ```settings.py``` otherwise you won't be able to create users (service 
is sending activation link to users)

### Docker installation

In ```settings.py``` file (lines ~120-130), change database for ```DOCKER DB```.  
REMEMBER to comment local database  
Now you are ready to go and able to run ```docker-compose up --build```  
Side note: In this case you need to create super user by running ```docker-compose run web python manage.py createsuperuser```
and after that, start server again with ```docker-compose up```.

### Manual installation
Create virtual environment on your machine, then install requirements using:
```
pip install -r requirements.txt
```
Open terminal in ```manage.py``` directory and type ```python manage.py migrate```.
After that, fill database using ```python manage.py loaddata sample.json``` .
Run tests ```python manage.py test``` and finally start server by ```python manage.py runserver``` command.

## Built With

* [Django](https://www.djangoproject.com/)
