import pr0gramm
import data_collection

api = pr0gramm.API()
api.enableSFW()
api.disableVideos()

collector = data_collection.DataCollector(api)
last_id = collector.collectDataBatch()
