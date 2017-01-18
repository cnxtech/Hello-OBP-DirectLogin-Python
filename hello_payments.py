# -*- coding: utf-8 -*-

from __future__ import print_function    # (at top of module)
import sys, requests


# Note: in order to use this example, you need to have at least one account
# that you can send money from (i.e. be the owner).
# All properties are now kept in one central place

from props.danskebank import *

# You probably don't need to change those
import lib.obp
obp = lib.obp

obp.setBaseUrl(BASE_URL)
obp.setApiVersion(API_VERSION)

# login and set authorized token
obp.login(USERNAME, PASSWORD, CONSUMER_KEY)

banks = obp.getBanks()

our_bank = banks[0]['id']
cp_bank = our_bank
print ("our bank: {0}".format(our_bank))

#get accounts for a specific bank
print (" --- Private accounts")

accounts = obp.getPrivateAccounts(our_bank)

for a in accounts:
    print (a['id'])

#just picking first account
our_account = accounts[0]['id']
cp_account = accounts[1]['id']
print ("our account: {0}".format(our_account))

print ("")
print (" --- Get owner transactions")
transactions = obp.getTransactions(our_bank, our_account) 
print ("Got {0} transactions".format(len(transactions)))

print (" --- Get challenge request types")
challenge_type = obp.getChallengeTypes(our_bank, our_account) 
print (challenge_type)

print ("")
print ("Initiate transaction requesti (small value)")
initiate_response = obp.initiateTransactionRequest(our_bank, our_account, challenge_type, cp_bank, cp_account) 

if "error" in initiate_response:
    sys.exit("Got an error: " + str(initiate_response))

if (initiate_response['challenge'] != None):
    #we need to answer the challenge
    challenge_query = initiate_response['challenge']['id']
    transation_req_id = initiate_response['id']['value']

    challenge_response = obp.answerChallenge(bank, account, transaction_req_id, challenge_query) 
    if "error" in challenge_response:
        sys.exit("Got an error: " + str(challenge_response))

    print ("Transaction status: {0}".format(challenge_response['status']))
    print ("Transaction created: {0}".format(challenge_response["transaction_ids"]))
else:
    #There was no challenge, transaction was created immediately
    print ("Transaction was successfully created: {0}".format(initiate_response["transaction_ids"]))

