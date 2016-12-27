import argparse
import pr0gramm
import data_collection


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
                        help="the type of source that should be used when downloading media (0=IMAGE, 1=THUMBNAIL, 2=FULL_SIZE)",
                        type=int, choices=range(3))

    parser.add_argument("--no_download", "-nd",
                        help="disables downloading the media content for submissions", action="store_true")
    parser.add_argument(
        "--save_json", "-sj", help="enables saving the retrieved json content locally", action="store_true")
    parser.add_argument("--use_local_storage", "-l",
                        help="enables using previously locally stored json contents instead of retrieving remotely",
                        action="store_true")

    parser.add_argument(
        "--frequency", "-f", help="set the frequency of lookups in hours (Default: 5)", type=int, default=5)

    args = parser.parse_args()
    run_collection_process(args)


def run_collection_process(args):
    pass


if __name__ == "__main__":
    main()
