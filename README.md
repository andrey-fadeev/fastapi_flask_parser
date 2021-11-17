This is educational repo to demonstrate how easy is to use fastapi (or flask), celery, docker and docker-compose, pytest  

POST /tags accept website url in json format and return task id. Example request:  
{"website": "https://google.com"}  

GET /tags/<task_id> return number of each HTML element or task status if its in progress  

RUN:  
- ```docker-compose up```

- ```pytest -m webtest```  
or simply:  
```pytest```

This will run and test FastApi implementation. Alternatively, you can use Flask one:
- ```docker-compose -f docker-compose.flask.yml up```
- ```pytest -m webtest --port=5000```  
