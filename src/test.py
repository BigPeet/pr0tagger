import pr0gramm

api = pr0gramm.API()
api.enableSFW()
items = api.getItems(tags="", user="", older="", newer="204777")

for item in items:
    print item.description()
