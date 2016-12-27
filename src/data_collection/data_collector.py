from datetime import timedelta
import json


__author__ = "Peter Wolf"
__mail__ = "pwolf2310@gmail.com"
__date__ = "2016-12-26"


class DataSources:
    IMAGE, THUMBNAIL, FULL_SIZE = range(3)


class DataCollector:

    """ The DataCollector retrieves relevant data from
        pr0gramm and saves it locally.
    """

    def __init__(self, api, last_id=None):
        self.api = api
        self.last_id = last_id
        self.age_threshold = timedelta(hours=5)
        self.search_forwards = True
        self.media_directory = "/tmp"
        self.data_source = DataSources.IMAGE
        self.annotation_file = "/tmp/annotation.txt"

    def setAgeThreshold(days=0, hours=5, minutes=0, seconds=0):
        self.age_threshold = timedelta(
            days=days, hours=hours, minutes=minutes, seconds=seconds)

    def setLastId(self, last_id):
        self.last_id = last_id

    def getLastId(self):
        return self.last_id

    def useBackwardsSearch(self):
        self.search_forwards = False

    def useForwardsSearch(self):
        self.search_forwards = True

    def setMediaDirectory(self, directory):
        self.media_directory = directory

    def setDataSource(self, source):
        self.data_source = source

    def setAnnotationFile(self, annotation_file):
        self.annotation_file = annotation_file

    def download(self, item):
        if self.data_source == DataSources.IMAGE:
            return self.api.downloadMedia(
                item, save_dir=self.media_directory, file_name=item.id)
        elif self.data_source == DataSources.THUMBNAIL:
            return self.api.downloadThumbnail(
                item, save_dir=self.media_directory, file_name=item.id)
        elif self.data_source == DataSources.FULL_SIZE:
            return self.api.downloadFullsize(
                item, save_dir=self.media_directory, file_name=item.id)
        else:
            print "No valid data source chosen!"
            return None

    def writeAnnotation(self, item, media_path):
        # write every item as a line with the following structure:
        # ID;IMAGE_PATH;AMOUNT_OF_TAGS;...TAG_TEXT;TAG_CONFIDENCE;...
        #TODO: maybe handle duplicate entries
        with open(self.annotation_file, "a") as f:
            line = str(item.id) + ";" + str(media_path) + \
                ";" + str(len(item.tags)) + ";"
            line += ";".join([str(tag.getText()) + ";" +
                              str(tag.getConfidence()) for tag in item.tags])
            f.write(line + "\n")

    def collectDataBatch(self):
        data = []
        if self.search_forwards:
            data = self.api.getItemsNewer(self.last_id)
        else:
            data = self.api.getItemsOlder(self.last_id)

        # filter data based on age and tags
        valid_data = []
        for item in data:
            if item.getAge() >= self.age_threshold and len(item.tags) > 0:
                valid_data.append(item)

        if not valid_data:
            return

        # save id of last item to fit age criteria in search direction
        if self.search_forwards:
            self.last_id = valid_data[0].getSortId()
        else:
            self.last_id = valid_data[-1].getSortId()

        # download media
        for item in valid_data:
            target_path = self.download(item)
            if target_path:
                # write id(s), link to media and tags to file
                self.writeAnnotation(item, target_path)

        return self.last_id
