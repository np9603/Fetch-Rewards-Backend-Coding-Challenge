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

