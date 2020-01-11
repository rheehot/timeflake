import argparse
from argparse import RawTextHelpFormatter

import timeflake
from timeflake.flake import DEFAULT_ALPHABET
from timeflake.utils import atoi


def main():
    DESCRIPTION = """Timeflakes are 64-bit (unsigned), roughly-ordered, globally-unique, URL-safe IDs."""

    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=1,
        help="the number of ids to generate (default: 1)",
    )
    parser.add_argument(
        "-s",
        "--shard-id",
        type=int,
        default=0,
        help="the shard id to use (default: random)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="include additional info for generated IDs",
    )

    args = parser.parse_args()

    instance = timeflake.Timeflake(shard_id=args.shard_id if args.shard_id else None)

    for _ in range(args.num):
        if args.shard_id:
            value = instance.next()
        else:
            value = instance.random()
        if args.verbose:
            timestamp, shard_id, counter = instance.parse(value)
            decoded = ""
            if instance._encoded:
                decoded = f" decoded={atoi(value, DEFAULT_ALPHABET)}"
            print(
                f"id={value}{decoded} timestamp={timestamp} shard_id={shard_id} counter={counter}"
            )
        else:
            print(value)


if __name__ == "__main__":
    main()
