This API service is written to run under Python 3.

*Installation*
----------------------------------
```
cd micro_url/
python3 setup.py install
```

*Running the service*
----------------------------------
The service will be available on http://localhost:8000
```
cd micro_url/micro_url/
python3 api.py
```

*Querying the API*
----------------------------------
Doing a GET to the root of the API will return a json list of shortened URLs
- GET http://localhost:8000

Doing a POST to the root of the API will return a json object containing the shortened URL
- POST http://localhost:8000
- RAW POST BODY: {'mobile' : '', 'tablet' : '', desktop : 'google.com'}
- RESPONSE: {'shortened_url' : 'http://localhost:8000/asdf'}