from twython import TwythonStreamer
import json

# appending data to a global variable is pretty poor form
# but it does make life easier

tweets = []
with open('credentials.json', 'r') as f:
    datastore = json.load(f)

class MyStreamer(TwythonStreamer):
    """our own subclass of twythonstreamer that specifies how to interact with the stream"""

    def on_success(self,data):
        """what do when twitter sends us data?"""

        if data['lang'] == 'en': #only want english tweets
            tweets.append(data)
            print("Recieved tweet #", len(tweets))

        #stop when we have enough
        if len(tweets) >= 10:
            self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

stream = MyStreamer(datastore['apiKey'], datastore['apiSecretKey'], datastore['accessToken'], datastore['accessTokenSecret'])

#starts consuming public statuses that contain the keyword 'data'
stream.statuses.filter(track='vote')

print(tweets[-1]['text'])
