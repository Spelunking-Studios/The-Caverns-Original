class KeyManager:
    """Manages keys"""
    def __init__(self, game):
        """Initialize the key manager"""
        self.game = game
        self.keys = {}
    def setKey(self, keyName, keyValue):
        """Set a key (keyName) to a value (keyValue)
        
        Arguments:
        -----
        keyName: string
            The keyname
        keyValue: boolean
            The value (True or False)
        """
        self.keys[keyName] = keyValue
    def getKey(self, keyName):
        """Returns a boolean describling if the key is pressed
        
        Arguments:
        -----
        keyName: string
        """
        try:
            v = self.keys[keyName]
        except KeyError:
            v = False
        return v