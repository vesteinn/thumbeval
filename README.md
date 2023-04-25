# thumbeval
*rudimentary readme -- more to follow*


```bash
# install django
pip install django

# populate sqlite database
python manage.py migrate 

# load data
python manage.py load_captions file_name.. model_name..

# create superuser
python manage.py createsuperuser

# run development server
python manage.py runserver
```

Then navigate to `127.0.0.1:8000/admin` to log in
