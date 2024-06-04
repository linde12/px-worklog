import os
import argparse
import logging

from pydantic import ValidationError
from lib import PxClient, PxSettings

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    # required
    parser.add_argument("-u", "--username", help="the username to be used for logging in", type=str, required=True)
    parser.add_argument("-w", "--week", help="the year-week combo (YYYYWW) to report hours for, e.g. 202425", type=int, required=True)
    parser.add_argument("--project", help="the project to use for reporting", type=str, required=True)
    parser.add_argument("--activity", help="the activity to use for reporting", type=str, required=True)

    # optionals
    parser.add_argument("--database", help="the database to use", default="stsoft", type=str)
    parser.add_argument("--server", help="the server to use", default="px", type=str)
    parser.add_argument("--url", help="the base url to use, e.g. https://px.mycompany.se", default="https://px.sigmatechnology.se", type=str)
    args = parser.parse_args()

    weekstr = str(args.week)
    if len(weekstr) != 6:
        logger.error("week must be in the format YYYYWW")
        return

    if not os.environ.get("PX_PASSWORD"):
        logger.error("PX_PASSWORD environment variable not set. Exiting.")
        return

    settings = PxSettings(
        base_url=args.url,
        username=args.username,
        password=os.environ["PX_PASSWORD"],
        server=args.server,
        database=args.database,
        project=args.project,
        activity=args.activity,
    )

    client = PxClient(settings).login()
    response = client.report_hours(weekstr, 8)
    if response.status_code == 200:
        logger.info('Hours reported successfully. Please verify')


if __name__ == "__main__":
    main()
