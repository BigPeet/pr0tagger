import pr0gramm
import data_collection

api = pr0gramm.API()
api.enableSFW()
api.disableVideos()

collector = data_collection.DataCollector(api)
collector.setDataSource(data_collection.DataSources.THUMBNAIL)
last_id = collector.collectDataBatch(download=False, save_json=True, local_data=False)
