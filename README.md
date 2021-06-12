# Fetch-Rewards-Backend-Coding-Challenge

This documentation explains how to setup your system to run the Flask web service. 

# Requirements

Python 3.7 - https://www.python.org/downloads/release/python-379/

Install python based on the instructions given in the above mentioned url. Make sure you set the python path in your environment variables properly. 

Download all the files (download ZIP), open command prompt and then navigate to the project folder.

After installing python on your system, we need to install some additional modules for running the Flask webservice. To install the additional modules, run the following command in the command prompt: 

```
pip install -r requirements.txt
```

# Assumptions/Key Notes 

1. All transactions have payer (string), points (integer) and timestamp (string) in the proper format. 

2. Add transactions takes in all transactions (even if negative transactions are coming first). The reason for this implementation is because we need to make sure that we do not eliminate transactions that actually have older timestamps and could have been included as correct transactions if newer transactions would eventually make the total points positive. 

3. Display points balance
  - If we want to check balance just after adding transactions and before spending, use show_initial_balance.
  - If we want to check balance after spending points, use show_balance.
  
# Starting the web service

After installing the additional modules required for the project, run the following command to start the Flask app:

```
python webservice.py
```

The web service is now running on the url http://127.0.0.1:5000/ 

```
 * Serving Flask app "Flask_app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 308-345-048
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 ```

# Testing the web service using test_webservice.py file

The test_webservice file tests all the API endpoints (add transaction, spend points, show balance, show initial balance)

```
pytest test_webservice.py
```

You will see an output like this indicating all the test cases passed. 

```
================================================= test session starts =================================================
platform win32 -- Python 3.7.9, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: D:\Github\Fetch-Rewards-Backend-Coding-Challenge
collected 3 items

test_webservice.py ...                                                                                           [100%]

================================================== 3 passed in 0.27s ==================================================
```

# Testing the web service using cURL commands

1. Add transactions 

Endpoint

```
/add_transaction
```

Command

```
curl -i -H "Content-Type: application/json" --data "{\"payer\": \"DANNON\", \"points\":1000, \"timestamp\": \"2020-11-02T14:00:00Z\"}" -X POST http://127.0.0.1:5000/add_transaction
```
```
curl -i -H "Content-Type: application/json" --data "{\"payer\": \"UNILEVER\", \"points\":200, \"timestamp\": \"2020-10-31T11:00:00Z\"}"  -X POST http://127.0.0.1:5000/add_transaction
```
```
curl -i -H "Content-Type: application/json" --data "{\"payer\": \"DANNON\", \"points\":-200, \"timestamp\": \"2020-10-31T15:00:00Z\"}" -X POST http://127.0.0.1:5000/add_transaction
```
```
curl -i -H "Content-Type: application/json" --data "{\"payer\": \"MILLER COORS\", \"points\":10000, \"timestamp\": \"2020-11-01T14:00:00Z\"}" -X POST http://127.0.0.1:5000/add_transaction
```
```
curl -i -H "Content-Type: application/json" --data "{\"payer\": \"DANNON\", \"points\":300, \"timestamp\": \"2020-10-31T10:00:00Z\"}" -X POST http://127.0.0.1:5000/add_transaction
```

Response

```
Successfully added transaction record to the main database
```

2. Show initial balance

Endpoint

```
/show_initial_balance
```

Command

```
curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/show_initial_balance
```

Response

```
{
  "DANNON": 800,
  "MILLER COORS": 10000,
  "UNILEVER": 200
}
```

3. Spend points

Endpoint

```
/spend_points
```

Command

```
curl -i -H "Content-Type: application/json" --data "{\"points\": 5000}" -X DELETE http://127.0.0.1:5000/spend_points
```

Response

```
[
  {
    "payer": "DANNON",
    "points": -100
  },
  {
    "payer": "UNILEVER",
    "points": -200
  },
  {
    "payer": "MILLER COORS",
    "points": -4700
  }
]
```

4. Show balance

Endpoint

```
/show_balance
```

Command

```
curl -i -H "Content-Type: application/json" http://127.0.0.1:5000/show_balance
```

Response

```
{
  "DANNON": 1000,
  "MILLER COORS": 5300,
  "UNILEVER": 0
}
```

# References

- https://docs.pytest.org/en/6.2.x/index.html
- https://medium.com/analytics-vidhya/how-to-test-flask-applications-aef12ae5181c
