"""

Simple Python Pr0gramm-API Wrapper expanding on
python-pr0gramm-api by David Mann <daaavid.mann@gmail.com>
(see https://github.com/davidmann4/python-pr0gramm-api)

"""

import json
import requests
from Item import Item

PROTOCOL_PREFIX = "http://"
SECURE_PROTOCOL_PREFIX = "https://"
HOST_NAME = "pr0gramm.com"


class API:

    def __init__(self):
        self.protocol_prefix = PROTOCOL_PREFIX
        self.sfw = True
        self.nsfw = False
        self.nsfp = False
        self.nsfl = False
        self.promoted = True

    def getBaseAPIUrl(self):
        return self.protocol_prefix + HOST_NAME + "/api"

    def getImageUrlPrefix(self):
        return self.protocol_prefix + "img." + HOST_NAME

    def getThumbUrlPrefix(self):
        return self.protocol_prefix + "thumb." + HOST_NAME

    def getFullSizeUrlPrefix(self):
        return self.protocol_prefix + "full." + HOST_NAME

    def enableSFW(self):
        self.sfw = True

    def disableSFW(self):
        self.sfw = False

    def enableNSFW(self):
        self.nsfw = True

    def disableNSFW(self):
        self.nsfw = False

    def enableNSFL(self):
        self.nsfl = True

    def disableNSFL(self):
        self.nsfl = False

    def enableNSFP(self):
        self.nsfp = True

    def disableNSFP(self):
        self.nsfp = False

    def setPromoted(self, value):
        self.promoted = value

    def getFlags(self):
        flags = 0
        if self.sfw:
            flags = 1
        if self.nsfw:
            flags += 2
        if self.nsfl:
            flags += 4
        if self.nsfp:
            flags += 8
        return flags

    def createMockItem(self):
        return Item.mockItem()

    def getAllImagesNewer(self, timestamp):
        return self.getItemsNewer(timestamp, videos=False)

    def getAllImagesOlder(self, timestamp):
        return self.getItemsOlder(timestamp, videos=False)

    def getItemsNewer(self, timestamp, tags="", user="", images=True, videos=True):
        return self.getItems(
            tags=tags, user=user, newer=timestamp, images=images, videos=videos)

    def getItemsOlder(self, timestamp, tags="", user="", images=True, videos=True):
        return self.getItems(
            tags=tags, user=user, older=timestamp, images=images, videos=videos)

    def getItems(self, tags="", user="", older="", newer="", images=True, videos=True):
        items = self.search(tags, user, older, newer)
        for item in items:
            if (item.isImage() and images) \
                    or (item.isVideo() and videos):
                item.setTagsFromJSON(self.getTags(item.id))
            else:
                items.remove(item)
        items.sort(reverse=True)
        return items

    def search(self, tags="", user="", older="", newer=""):
        args = {
            'flags': self.getFlags(),
            'tags': tags,
            'user': user,
        }
        if older:
            args["older"] = older
        if newer:
            args["newer"] = newer
        if self.promoted:
            args["promoted"] = 1

        url = self.getBaseAPIUrl() + "/items/get"
        response = requests.get(url, params=args)
        response.raise_for_status()
        search_results = []
        for item in response.json()["items"]:
            search_results.append(Item.parseFromJSON(item))
        return search_results

    def getInfo(self, post_id):
        args = ({
            'itemId': post_id
        })

        url = self.getBaseAPIUrl() + "/items/info"
        response = requests.get(url, params=args)
        response.raise_for_status()
        return response.json()

    def getTags(self, post_id):
        info = self.getInfo(post_id)
        return info["tags"]

    def downloadMedia(self, item, save_dir=".", file_name="", extension=""):
        image_url = self.getImageUrlPrefix() + "/" + item.image_link
        if not file_name:
            file_name = item.image_link.split("/")[-1]
        if not extension:
            extension = item.image_link.split(".")[-1]
        target_path = str(save_dir) + "/" + str(file_name) + "." + str(extension)
        with open(target_path, "wb") as f:
            f.write(requests.get(image_url).content)

