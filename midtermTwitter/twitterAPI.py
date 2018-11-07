from twython import TwythonStreamer
import io, json

# appending data to a global variable is pretty poor form
# but it does make life easier

with open('credentials.json', 'r') as f:
    datastore = json.load(f)

class MyStreamer(TwythonStreamer):
    tweets = 0
    """our own subclass of twythonstreamer that specifies how to interact with the stream"""
    def on_success(self,data):
        """what do when twitter sends us data?"""
        self.tweets+= 1
        try:
            if data['lang'] == 'en': #only want english tweets
                with io.open('../../../../../../../Volumes/jakesExternalDrive/tweets.txt', 'a', encoding='utf-8') as f:
                    f.write(json.dumps(data, ensure_ascii=False))
                    f.write('\n'.decode('utf-8'))
                    f.write('\n'.decode('utf-8'))
                print("Recieved tweet #"+str(self.tweets))
        except:
                print("???")


#self.disconnect()

    def on_error(self, status_code, data):
        print("ERROR #1")
        print(status_code, data)
        self.disconnect()

stream = MyStreamer(datastore['apiKey'], datastore['apiSecretKey'], datastore['accessToken'], datastore['accessTokenSecret'])

#starts consuming public statuses that contain the keyword 'data'
while True:
    try:
        stream.statuses.filter(track='vote')
    except:
        print("ERROR #2")

