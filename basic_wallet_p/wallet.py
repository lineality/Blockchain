# class lecture solution
import hashlib
import requests
import sys
import json

if __name__ == "__main__":
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    user_id = f.read()
    print("ID is", user_id)
    f.close()

    the_current_balance = 0

    # 2. a REPL loop :
    # Read
    # Evaluate
    # Print
    # Loop
    while True:

        # Ask for user name update:
        # Print the current description
        print("Login: Enter User Name")
        print("My name is should be... (fees may apply)")
        # this is what the player will do
        user_id = input("-> ")

        # Get the Chain
        r = requests.get(url=node + "/chain")
        # Handle non-json response (stretch)
        whole_chain_json = r.json()

        # print test
        print("This is the whole chain: ", whole_chain_json)
        print("\n")
        print("\n")

        # # # traverse list and get all transactions entries
        # for i in whole_chain_json["chain"]:
        #     print(i["transactions"])

        intransactions = whole_chain_json["chain"]

        print("Here are all user transactions:")
        # prints all user transactions
        # user_id = "gga"
        for i in intransactions[1:]:
            if (
                i["transactions"][0]["recipient"] == user_id
                or i["transactions"][0]["sender"] == user_id
            ):
                print(i["transactions"][0])
        print("\n")
        print("\n")

        # prints all user transactions
        current_total = 0
        # user_id = "gga"
        for i in intransactions[1:]:
            if i["transactions"][0]["recipient"] == user_id:
                current_total += i["transactions"][0]["amount"]
            if i["transactions"][0]["sender"] == user_id:
                current_total -= i["transactions"][0]["amount"]
        print("this is the current balance of the user")
        print("recipients - senders", current_total)
        print("\n")
        print("\n")
        #
        # # READ
        # print(f"Hello, {user_id}. Let's Transaction!")
        #
        # # Print the current description
        # print("Who is the recipient?")
        # print("Enter name of recipient: (fees may apply)")
        # # this is what the player will do
        # recipient = input("-> ")
        #
        # # Print the current description
        # print("What is the amount?")
        # # this is what the player will do
        # transaction_amount = int(input("-> "))
        #
        # # EVALUATE
        #
        # # url =
        # # # this assumes that the agreed upon json key is `input`
        # val = {
        #     "sender": user_id,
        #     "recipient": recipient,
        #     "amount": transaction_amount,
        # }  # '' is used within a route like a dictionary key
        # url = node + "/transactions/new"
        # r_success = requests.post(url, data=json.dumps(val))
        #
        # # inspection
        # print(val)
        #
        # # required = ["sender", "recipient", "amount"]
        # print(
        #     f"request responded: {r_success}.\nthe content of the response was {r_success.json()}"
        # )
