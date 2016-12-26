import pr0gramm

# Requests items older than some promoted tag
api = pr0gramm.API()
api.enableSFW()
items = api.getItemsOlder("204477")
print items[0].description()



# Tests with Mock Object
mock = api.createMockItem()
print mock.description()
