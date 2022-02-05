#
#   These bits of code demonstrate the use of the Search object
#   from the file Search.py 
#
#   The code snippets are best used by copy and paste into the
#   python interpreter.
#
#   You can also just run the Search.py code at the command line
#   and read the main() code as an example
#
# Import some system modues and pieces of the mele user module.
# The following code depends on these modules.

#def main(argv):
#   <setup_code>
#   <your_collector_loop>
#       <search_to_collect_tweets>
#       <your_uniqueness_check>
#       <reformat_tweets>
#       <save_tweets>
#       <sleep_10_seconds>
#   <closing_code>

#
#
#
import sys, json, pickle
from mele.twit.Authorizer import Authorizer
from mele.twit.Search import Search
from mele.twit.support import *
#
# Next create an authorized login object
# Need a couple variables to represent the app and user
app = "HCDE530Test01"
user = "dwmcphd" # this is my twitter user, you should use your own here
#
def set_up():
# Get the application keys - this comes from mele.twit.support
    app_keys = TWITTER_APP_OAUTH_PAIR(app=app)
    #
    # Now create an authentication object, we'll need it to authenticate twitter requests
    auth = Authorizer(name="auth for Search", app_name=app, app_user=user)
    auth.setConsumerKey(app_keys['consumer_key'])
    auth.setConsumerSecret(app_keys['consumer_secret'])
    auth.authorize()

    #
    # Next we create a new search object and set some required
    # object values to enable a search
    search = Search()
    search.setAuthObject(auth)              # Add the authentication object
    search.setThrottling(True)              # throttle the requests
    search.setQueryResultType(rt="recent")  # we want the most recent tweets not 'popular' ones
    search.setPageSize(sz=100)
    #
    # This is the part you expected, we set some search terms, just
    # one term in this specific case
    terms = "olympic"
    search.setQueryTerms(terms)
    return search 


import time
def collection_loop(search=None, loops=10, fname="data"):
    cycles = 5
    total = 0
    count = 0  
    while(cycles <= loops): 
        print("Making request %d"%(count))
        search.makeRequest()
        response = search.getMessage()
        if( response ):
            print("\tGot %d tweets this time."%(len(response)))
            total = total + len(response)
            print("\tHave %d total tweets."%(total))
            data_fname = fname+"%04d.pickle"%(count)
            pickle_data(data_fname,response)
        else:
            print("No response this cycle (%d)"%(cycles))
        time.sleep(10.0)
        cycles += 1

        #uniqness_check
        results = []
        tracking_dictionary ={"id":[]};
        for tweet in response:
        # Here, we convert the dictionary back to JSON so that it
        # prints nicely on the screen
            #tracking_dictionary['id'] = tweet['id']
                for key,value in tracking_dictionary:
                        if value not in tracking_dictionary:
                            tracking_dictionary['id'].append(tweet['id'])
                            results.append(tweet['full_text'])
                #print(response)
                print(results)
                print(tracking_dictionary)
                #print(json.dumps(tweet,indent=4,sort_keys=True))
                #print(len(response))
    return total

# Now that we've collected some tweets we need a way to save them.
# One simple way that we saw earlier in class was to use pickle.
# This defines a simple little procedure that opens a file, writes
# the data as a pickle file.
def pickle_data(fname="",d={}):
    if( fname ):
        fout = open(fname, "wb")
        pickle.dump(d,fout)
        fout.close()
    else:
        print("Must supply a file name!")
    return
#
# Using the pickle_data() procedure we can easily save the tweets
# in the response. Note here that we're saving one whole data structure.
# The response variable was a Python list that contained up to 100 tweets
# each of which was a Python dictionary. Pickle is best if you're storing
# one whole Python data structure, even if that data structure has other
# data structures within it. Like our response.
#pickle_data("tweets.001.pickle",response)


if __name__ == '__main__':
    search_object = set_up()
    collection_loop(search_object)
