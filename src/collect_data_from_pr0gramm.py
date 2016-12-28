import sys
import time
import datetime
import argparse
import pr0gramm
import data_collection
import logging_setup
import logging

LOG = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Collect data from pr0gramm.com")

    parser.add_argument(
        "--no_sfw", help="disable SFW content", action="store_true")
    parser.add_argument(
        "--nsfw", help="enable NSFW content", action="store_true")
    parser.add_argument(
        "--nsfl", help="enable NSFL content", action="store_true")

    parser.add_argument(
        "--no_images", help="disable images", action="store_true")
    parser.add_argument(
        "--allow_videos", help="enable video content", action="store_true")

    parser.add_argument(
        "--last_id", "-id", help="the last promoted id use as anchor point", type=int, default=None)
    parser.add_argument("--age_threshold", "-age",
                        help="a submission must be the given amount of hours old to be downloaded (Default: 5)",
                        type=int, default=5)
    parser.add_argument("--min_num_of_tags", "-min",
                        help="a submission must have the given amount of tags to be downloaded (Default: 5)",
                        type=int, default=5)
    parser.add_argument(
        "--search_backwards", help="search for submission older than last_id, instead of newer", action="store_true")

    parser.add_argument("--media_directory", "-o",
                        help="the download directory for media content (images, videos)", type=str, default="/tmp")
    parser.add_argument("--annotation_file", "-ann",
                        help="the annotation file that should be created/edited for the downloaded media content",
                        type=str, default="/tmp/annotation.txt")
    parser.add_argument("--json_directory", "-jd",
                        help="the download directory for the retrieved json content", type=str, default="/tmp")
    parser.add_argument("--data_source", "-ds",
                        help="the type of source that should be used when downloading media (0=IMAGE, 1=THUMBNAIL, 2=FULL_SIZE), Default: 0",
                        type=int, choices=range(3), default=0)

    parser.add_argument("--no_download", "-nd",
                        help="disables downloading the media content for submissions", action="store_true")
    parser.add_argument(
        "--save_json", "-sj", help="enables saving the retrieved json content locally", action="store_true")
    parser.add_argument("--use_local_storage", "-l",
                        help="enables using previously locally stored json contents instead of retrieving remotely",
                        action="store_true")

    parser.add_argument(
        "--waiting_time", "-t", help="set the waiting time for lookups in hours (Default: 5)", type=int, default=5)

    parser.add_argument("logging_json_config", "-lc",
                        help="the logging json dictionary used to initialize the logging framework (Default: ../etc/logging.json)",
                        type=str,
                        default="../etc/logging.json")

    parser.add_argument("logging_file", "-lf",
                        help="specify a log file, per default the log file is chosen based on the logging_json_config",
                        type=str,
                        default=None)

    logging_setup.setup_logging(args.logging_json_config, log_file=args.logging_file)
    args = parser.parse_args()
    run_collection_process(args)


def run_collection_process(args):
    collector = initialize_collector(args)
    waiting_time_in_seconds = args.waiting_time * 60 * 60

    while(True):
        LOG.info("Start collecting from ID: {}.".format(collector.getLastId()))
        collector.collectDataBatch()
        LOG.info("Collected {0} item(s). Last ID: {1}".format(
            collector.getSizeOfLastBatch(),
            collector.getLastId()))
        LOG.info("Going to sleep for {0} hours until {1}.".format(
            args.waiting_time,
            datetime.datetime.now() + datetime.timedelta(hours=args.waiting_time)))

        if collector.getSizeOfLastBatch() <= 0:
            # TODO: give some status updates while waiting
            time.sleep(waiting_time_in_seconds)


def initialize_collector(args):
    api = initialize_api(args)

    collector = data_collection.DataCollector(api)
    collector.setLastId(args.last_id)
    collector.setAgeThreshold(hours=args.age_threshold)
    collector.setMinimumNumberOfTags(args.min_num_of_tags)
    if args.search_backwards:
        collector.useBackwardsSearch()
    collector.setMediaDirectory(args.media_directory)
    collector.setAnnotationFile(args.annotation_file)
    collector.setJsonDir(args.json_directory)
    collector.setDataSource(args.data_source)
    collector.setDownloadMedia(not args.no_download)
    collector.setSaveJSON(args.save_json)
    collector.setUseLocalStorage(args.use_local_storage)

    return collector


def initialize_api(args):
    api = pr0gramm.API()
    if args.no_sfw:
        api.disableSFW()
    if args.nsfw:
        api.enableNSFW()
    if args.nsfl:
        api.enableNSFL()
    if args.no_images:
        api.disableImages()
    if args.allow_videos:
        api.enableVideos()

    return api


if __name__ == "__main__":
    main()
