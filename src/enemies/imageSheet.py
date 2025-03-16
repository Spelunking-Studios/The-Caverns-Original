class ImageSheet:
    def __init__(self, images = {}):
        self.images = images
    def addImage(self, key, image):
        self.image[key] = image
    def getImage(self, key):
        try:
            return self.images[key]
        except KeyError:
            return None

class BossImageSheet(ImageSheet):
    def __init__(self, images = {}):
        super().__init__({})
