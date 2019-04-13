class TestLinstener:
    def __init__(self, username):
        self.__username = username
        print("Hi "+self.__username)

    def ReadMessage(self, event):
        print("%s Got a Message" % self.__username)
        print("Content: %s" % event.data["Event"])
