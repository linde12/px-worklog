import argparse
import logging

from pydantic import ValidationError
from lib import PxClient, PxSettings

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--week", help="the year-week combo (YYYYWW) to report hours for, e.g. 202425", type=int)
    parser.add_argument("-u", "--username", help="The username to be used for logging in", type=str)
    args = parser.parse_args()
    weekstr = str(args.week)

    if len(weekstr) != 6:
        logger.error("week must be in the format YYYYWW")
        return

    try:
        settings = PxSettings(
            base_url="https://px.sigmatechnology.se",
            username=args.username,
            # password="from_env_var",
            server="px",
            database="stsoft",
            project="189268",
            activity="3",
        ) # pyright: ignore
    except ValidationError as e:
        missing = ", ".join([str(error["loc"][0]) for error in e.errors()])
        logger.error(f"Missing environment variables: {missing}. Exiting.")
        return

    client = PxClient(settings).login()
    response = client.report_hours(weekstr, 8)
    if response.status_code == 200:
        logger.info('Hours reported successfully. Please verify')


if __name__ == "__main__":
    main()
