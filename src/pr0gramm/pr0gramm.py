"""

Simple Python Pr0gramm-API Wrapper expanding on
python-pr0gramm-api by David Mann <daaavid.mann@gmail.com>
(see https://github.com/davidmann4/python-pr0gramm-api)

"""

__author__ = "Peter Wolf"
__mail__ = "pwolf2310@gmail.com"
__date__ = "2016-12-25"

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
        self.images = True
        self.videos = True

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

    def enableImages(self):
        self.images = True

    def disableImages(self):
        self.images = False

    def enableVideos(self):
        self.videos = True

    def disableVideos(self):
        self.videos = False

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

    def getItemsNewer(self, item_id, tags="", user=""):
        return self.getItems(
            tags=tags, user=user, newer=item_id)

    def getItemsOlder(self, item_id, tags="", user=""):
        return self.getItems(
            tags=tags, user=user, older=item_id)

    def getItems(self, tags="", user="", older="", newer=""):
        items = self.search(tags, user, older, newer)
        for item in items:
            if (item.isImage() and self.images) \
                    or (item.isVideo() and self.videos):
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
        url = self.getImageUrlPrefix() + "/" + item.getMediaLink()
        return self.download(url, save_dir, file_name, extension)

    def downloadThumbnail(self, item, save_dir=".", file_name="", extension=""):
        url = self.getThumbUrlPrefix() + "/" + item.getThumbnailLink()
        return self.download(url, save_dir, file_name, extension)

    def downloadFullsize(self, item, save_dir=".", file_name="", extension=""):
        if item.getFullsizeLink():
            url = self.getFullSizeUrlPrefix() + "/" + item.getFullsizeLink()
            return self.download(url, save_dir, file_name, extension)
        else:
            return self.downloadMedia(item, save_dir, file_name, extension)

    def download(self, url, save_dir, file_name="", extension=""):
        if not file_name:
            # take the file name from the url, but remove extension
            # in case some other extension is provided
            file_name = url.split("/")[-1]
            file_extension = "." + file_name.split(".")[-1]
            file_name = file_name[:-len(file_extension)]
        if not extension:
            # take the extension from the url
            extension = url.split(".")[-1]
        target_path = str(save_dir) + "/" + \
            str(file_name) + "." + str(extension)
        with open(target_path, "wb") as f:
            f.write(requests.get(url).content)
        return target_path
