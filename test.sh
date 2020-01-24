
unset SECRET_KEY
export $(xargs <.env)

# run flake8 test
flake8

# run django unitTest
python manage.py test