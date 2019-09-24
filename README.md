# Tails Assignment

## How to run with docker
```docker-compose up --build```

This will automatically setup the docker container and run load_stores management command to 
save stores from stores.json file and fetches latitude and longitude info for all stores
from Postcode.io 

### How to run test in docker container
```docker-compose run app python manage.py test```


## How to run locally on Mac or Linux

```
- Install virtualenv
pip install virtualenv
- Create virtualenv
virtualenv tails-env
- Activate virtualenv
source tails-env/bin/activate
- Install requirements
pip install -r requirements.txt
- Run migrations
python manage.py migrate
- Load stores
python manage.py load_stores
- Run development server
python manage.py runserver 0.0.0.0:8000
```

## Check store list using django rest framework template
http://localhost:8000/stores/

## Questions
### Tell us what test you completed (backend or full-stack)
* Backend

### Tell us what you'd have changed if you'd have had more time?
* I'd have done full stack task as well.
* I was planning to use stores api endpoint for both backend and full stack task. More info can be found on docstring.
* If I had time to do frontend task, I'd have done it using Vuejs. Though, the right decision would be using pure js, html, css for this lightweight task.
* Use flask instead of Django
* Make it production ready
* Load stores in parallel
* More tests
* More logging
* More detail documentation
* More detailed README.md

### What bits did you find the toughest? What bit are you most proud of? In both cases, why?
* Had to do some assumptions
-  Login not required
-  There is only one store in a postcode.
-  Project will be run in a machine that has access to the internet

### What's one thing we could do to improve this test?
* Measuring distance between two points requires geo knowledge which is not much related with development skills, it's hard to understand if it produces right result 
