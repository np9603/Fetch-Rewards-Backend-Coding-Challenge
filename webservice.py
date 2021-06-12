"""
Name - Nihal Surendra Parchand
Email - np9603@rit.edu
Version - Python 3.7

Background information to understand the problem -
- Users accumulate points in their accounts after making transactions (buying things) from several payers/partners
(we can imagine companies like Nike, Puma, Adidas).
- Each transaction record is in the form - payer (string), points (integer), and timestamp (date).
- The user does not care how the points are spent but the accounting team wants to keep track of how the points are
spent based on two conditions:

1. The oldest points (based on the transaction timestamps) should be spent first.
2. Payer's points should not go negative *while spending points*.

Goal of the task - Build a web service that accepts HTTP requests by providing three routes and returns responses based
on the conditions specified above.

ROUTES:
1. Add transactions for a specific payer and date.
2. Spend points using the rules above and return a list of { "payer": <string>, "points": <integer> } for each call.
3. Return all payer point balances.
(I have assigned two routes for returning the payer point balance - show_initial_balance and show_balance
show_initial_balance - Use this route if you want to check the payer balance before spending points
show_balance- Use this route if you want to check the balance after spending points)
"""

# Importing flask library to build the web service
from flask import Flask, request, jsonify

# Importing defauldict for storing points balance for each payer and deque for storing transactions
from collections import defaultdict, deque

# Extra libraries for further discussion
import json
import datetime

# Creating an instance of Flask class
app = Flask("Flask_app")

# Keep track of total points accumulated for the user
total_points = 0

# List to store all transactions
all_transactions = []

# Dictionary to store points balance for each payer. For ex: {'Nike':200}
payer_balance = defaultdict(int)

# Queue to maintain the order of final transactions after sorting them based on timestamps
final_transaction_queue = deque()

content_header = dict()
content_header["Content-Type"] = "application/json"


# Transaction class to store transaction details in the format - payer, points, timestamp
class Transaction:

    def __init__(self, payer, points, timestamp):
        self.payer = payer
        self.points = points
        self.timestamp = timestamp

    def get_payer(self):
        return self.payer

    def set_payer(self, payer):
        self.payer = payer

    def get_points(self):
        return self.points

    def set_points(self, points):
        self.points = points

    def get_timestamp(self):
        return self.timestamp

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    # For printing transaction objects
    def __str__(self):
        return "{'payer': '{%s}', 'points': {%d}, 'timestamp': '{%s}'}" % (self.payer, self.points, self.timestamp)


def sort_transactions(all_transactions):
    """
    This method takes a list of all transactions, sorts based on the timestamp (string comparison works perfectly but
    we can also typecast it to datetime objects for better understanding) and returns the sorted transactions list.
    :param all_transactions: list of all transactions
    :return: sorted_transactions: sorted (based on transaction timestamp) transactions list
    """
    sorted_transactions = sorted(all_transactions, key=lambda k: k["timestamp"])

    # sorted_transactions = sorted(all_transactions, key=lambda k: datetime.fromisoformat(k["timestamp"][:-1]))

    return sorted_transactions


def create_inputs(sorted_transactions):
    """
    This method iterates over the sorted transactions list to create:
    1 - payer_balance (dictionary) which stores points available for each payer
    2 - final_transaction_queue (deque) which stores the transactions based on their timestamps and takes care of
    negative points transactions
    :param sorted_transactions: sorted (based on transaction timestamp) transactions list
    :return: payer_balance: (dictionary) which stores points available for each payer
             final_transaction_queue: (deque) which stores the transactions based on their timestamps
    """

    global total_points

    for transaction in sorted_transactions:
        payer = transaction["payer"]
        points = int(transaction["points"])
        timestamp = transaction["timestamp"]

        """
        If points are positive: Update total points, balance of the payer and append transaction to the final transaction queue
        If points are negative:
            - If payer exists already and spending the current points makes the balance go negative: Insufficient balance error 
            - If payer exists already and spending the current points does not make the balance go negative: Update 
              total points, balance of the payer and traverse through the final transaction queue to update oldest
              transaction points (subtract oldest transaction points by current points to handle negative points)
            - If the payer does not exist: First transaction points can not be negative
        If points are zero: Simply print that it is a zero points transaction     
        """
        if points > 0:
            total_points += points
            payer_balance[payer] += points
            final_transaction_queue.append(Transaction(payer, points, timestamp))

        elif points < 0:
            if payer in payer_balance and payer_balance[payer] + points < 0:
                print("Insufficient balance error: 'payer': " + payer + " 'Current balance': " +
                      str(payer_balance[payer]) + " 'points': " + str(points))

            elif payer in payer_balance and payer_balance[payer] + points >= 0:
                total_points += points
                payer_balance[payer] += points
                for record in final_transaction_queue:
                    payer_name = record.get_payer()
                    if payer == payer_name:
                        remaining = record.get_points() + points
                        record.set_points(remaining)
                        break
            else:
                print("Invalid transaction error: First transaction points can not be negative")

        else:
            print("Zero points transaction")

    return payer_balance, final_transaction_queue


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    This is a REST endpoint that reads the transaction calls and stores it in the all_transaction list.
    :return: A success message with the OK status code (200)
    """

    transaction = request.get_json(force=True)
    all_transactions.append(transaction)

    return "Successfully added transaction record to the main database", 200, content_header


@app.route('/spend_points', methods=['DELETE'])
def spend_points():
    """
    This is a REST endpoint that receives points to be spent and returns a JSON object that shows the points spent by
    each payer based on the constraints mentioned in the background.
    :return: - Display an error with a status code (400) if the balance is insufficient
             - JSON object that displays payer name and the points deducted from that payer balance with a status code (200)
    """
    global total_points, payer_balance, final_transaction_queue

    data = request.get_json(force=True)
    points_to_spend = data["points"]

    # Sorting transactions based on timestamp
    sorted_transactions = sort_transactions(all_transactions)

    # Creating payer_balance, final_transaction_queue for further calculations
    payer_balance, final_transaction_queue = create_inputs(sorted_transactions)

    # If total points is less than the points to spend: Insufficient balance error
    if total_points < points_to_spend:
        return "Insufficient balance error", 400, content_header
    else:
        # List to store the points spent from each payer's balance
        answer_list = []

        # Iterate until we have points to spend
        while points_to_spend > 0:
            # Pop the oldest transaction and store the individual details
            transaction = final_transaction_queue.popleft()
            points = transaction.get_points()
            payer = transaction.get_payer()

            # Deduct current transaction points from the points to spend
            points_to_spend -= points

            # If points to spend goes negative (reached the end):
            if points_to_spend < 0:
                points_spent = points + points_to_spend
                transaction.set_points(-points_to_spend)
                final_transaction_queue.append(transaction)
            else:
                points_spent = points

            # Add a new transaction record with the current points spent in the answer list
            answer_list.append(
                Transaction(payer, points_spent, datetime.datetime.now().replace(microsecond=0).isoformat()))

            # Deduct the current points from the payer balance and total points
            payer_balance[payer] -= points_spent
            total_points -= points_spent

    # Adding a negative sign for each payer points that were spent
    for transaction in answer_list:
        points = transaction.get_points()
        transaction.set_points(-points)

    # Creating the response and sending it as a JSON serializable
    response = []
    for transaction in answer_list:
        response.append({"payer": transaction.get_payer(), "points": transaction.get_points()})
    return jsonify(response), 200, content_header


@app.route("/show_initial_balance", methods=['GET'])
def show_initial_balance():
    """
    This is a REST endpoint that returns a JSON object that shows the initial points balance for each payer before
    spending the points
    :return: JSON object that displays payer name and available points
    """
    balance = dict()

    # Sorting transactions based on timestamp
    sorted_transactions = sort_transactions(all_transactions)

    """ Iterate over the sorted transactions and check if:
        payer exists - add it to the existing points
        payer does not exist - create a record for the payer with current points
    """
    for transaction in sorted_transactions:
        payer = transaction["payer"]
        points = int(transaction["points"])
        if payer in balance:
            balance[payer] += points
        else:
            balance[payer] = points

    return jsonify(balance), 200, content_header


@app.route("/show_balance", methods=['GET'])
def show_balance():
    """
    This is a REST endpoint that returns a JSON object that shows the points balance for each payer
    :return: JSON object that displays payer name and available/remaining points after running spend points
    """

    return jsonify(payer_balance), 200, content_header


if __name__ == "__main__":
    """
    The main function is used to run the Flask web service/application
    """
    app.run(debug=True)
