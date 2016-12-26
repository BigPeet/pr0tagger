from Tag import Tag
import time

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class Item:

    """ An item retrieved from pr0gramm.com """

    def __init__(self, id):
        self.id = id
        self.tags = []
        self.promoted_stamp = None
        self.user = None
        self.created = None

        self.image_link = ""
        self.image_width = -1
        self.image_height = -1
        self.thumb_link = ""
        self.full_size_link = None
        self.source = None
        self.audio = False

        self.upvotes = -1
        self.downvotes = -1
        self.flags = 0

    def __str__(self):
        return "Item {0}, Promoted: {1}, Created: {3}, User: {2}".format(
            self.id, self.promoted_stamp, self.user,
            time.strftime(DATE_FORMAT, time.localtime(self.created)))

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def description(self):
        return "Item {0}, Promoted: {1}, Created: {3}, User: {2}\n".format(
            self.id, self.promoted_stamp, self.user,
            time.strftime(DATE_FORMAT, time.localtime(self.created))) \
            + "Image: {0} ({1}x{2})\n".format(
            self.image_link, self.image_width, self.image_height) \
            + "Thumb: {0}\n".format(self.thumb_link) \
            + "Full Size: {0}\n".format(self.full_size_link) \
            + "Source: {0}\n".format(self.source) \
            + "Flags: {0}, {1} Upvotes, {2} Downvotes\n".format(
                self.flags, self.upvotes, self.downvotes) \
            + "Tags: {}".format(", ".join([str(tag) for tag in self.tags]))

    def isImage(self):
        return self.image_link.endswith(".jpg") \
            or self.image_link.endswith(".png")

    def isVideo(self):
        return self.image_link.endswith(".mp4")

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
        parsed_item.promoted_stamp = json_item["promoted"]
        parsed_item.user = json_item["user"]
        parsed_item.created = json_item["created"]
        parsed_item.image_link = json_item["image"]
        parsed_item.image_width = json_item["width"]
        parsed_item.image_height = json_item["height"]
        parsed_item.thumb_link = json_item["thumb"]
        parsed_item.full_size_link = json_item["fullsize"]
        parsed_item.source = json_item["source"]
        parsed_item.audio = json_item["audio"]
        parsed_item.upvotes = json_item["up"]
        parsed_item.downvotes = json_item["down"]
        parsed_item.flags = json_item["flags"]
        return parsed_item
