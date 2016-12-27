from Tag import Tag
import time
from datetime import datetime

__author__ = "Peter Wolf"
__mail__ = "pwolf2310@gmail.com"
__date__ = "2016-12-25"


DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Item:

    """ An item retrieved from pr0gramm.com """

    def __init__(self, id):
        self.id = id
        self.tags = []
        self.promoted = None
        self.user = None
        self.created = None

        self.image = ""
        self.width = -1
        self.height = -1
        self.thumb = ""
        self.fullsize = None
        self.source = None
        self.audio = False

        self.up = -1
        self.down = -1
        self.flags = 0

    def __str__(self):
        return "Item {0}, Promoted: {1}, Created: {3}, User: {2}".format(
            self.id, self.promoted, self.user,
            time.strftime(DATE_FORMAT, time.localtime(self.created)))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def asDict(self):
        d = self.__dict__
        d["tags"] = [tag.__dict__ for tag in self.tags]
        return d

    def description(self):
        return "Item {0}, Promoted: {1}, Created: {3}, User: {2}\n".format(
            self.id, self.promoted, self.user,
            time.strftime(DATE_FORMAT, time.localtime(self.created))) \
            + "Image: {0} ({1}x{2})\n".format(
            self.image, self.width, self.height) \
            + "Thumb: {0}\n".format(self.thumb) \
            + "Full Size: {0}\n".format(self.fullsize) \
            + "Source: {0}\n".format(self.source) \
            + "Flags: {0}, {1} up, {2} down\n".format(
                self.flags, self.up, self.down) \
            + "Tags: {}".format(", ".join([str(tag) for tag in self.tags]))

    def isImage(self):
        return self.image.endswith(".jpg") \
            or self.image.endswith(".png")

    def isVideo(self):
        return self.image.endswith(".mp4") \
            or self.image.endswith(".gif")

    def getAge(self):
        return datetime.now() - datetime.fromtimestamp(self.created)

    def getSortId(self):
        return self.promoted

    def getMediaLink(self):
        return self.image

    def getThumbnailLink(self):
        return self.thumb

    def getFullsizeLink(self):
        return self.fullsize

    def setTagsFromJSON(self, json_tags):
        self.tags = []
        for json_tag in json_tags:
            self.tags.append(
                Tag(
                    json_tag["id"],
                    json_tag["confidence"],
                    json_tag["tag"]))

    @staticmethod
    def parseFromJSON(json_item):
        parsed_item = Item(json_item["id"])
        parsed_item.promoted = json_item["promoted"]
        parsed_item.user = json_item["user"]
        parsed_item.created = json_item["created"]
        parsed_item.image = json_item["image"]
        parsed_item.width = json_item["width"]
        parsed_item.height = json_item["height"]
        parsed_item.thumb = json_item["thumb"]
        parsed_item.fullsize = json_item["fullsize"]
        parsed_item.source = json_item["source"]
        parsed_item.audio = json_item["audio"]
        parsed_item.up = json_item["up"]
        parsed_item.down = json_item["down"]
        parsed_item.flags = json_item["flags"]
        parsed_item.tags = []
        if "tags" in json_item.keys():
            for json_tag in json_item["tags"]:
                tag = Tag(json_tag["id"],
                          json_tag["confidence"],
                          json_tag["tag"])
                parsed_item.tags.append(tag)

        return parsed_item

    @staticmethod
    def mockItem():
        mock = Item(1679829)
        mock.promoted = 204476
        mock.user = "ExampleUser"
        mock.created = 1482583310
        mock.image = "2016/12/24/058d591eb1eddbd3.mp4"
        mock.width = 640
        mock.height = 360
        mock.thumb = "2016/12/24/058d591eb1eddbd3.jpg"
        mock.fullsize = ""
        mock.source = ""
        mock.audio = False
        mock.up = 699
        mock.down = 11
        mock.flags = 1
        return mock
