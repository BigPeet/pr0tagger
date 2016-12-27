import pr0gramm
import data_collection

api = pr0gramm.API()
api.enableSFW()
api.disableVideos()

collector = data_collection.DataCollector(api)
collector.setDataSource(data_collection.DataSources.THUMBNAIL)
collector.setMediaDirectory("/tmp/test")
collector.setAnnotationFile("/tmp/test/annotation.txt")
last_id = collector.collectDataBatch()
