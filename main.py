import logging
from lib import PxClient, PxSettings

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    settings = PxSettings(
        base_url="https://px.sigmatechnology.se",
        username="OSL4642",
        password="OSL4642",
        server="px",
        database="stsoft",
        project="189268",
        activity="3",
    )
    client = PxClient(settings).login()
    response = client.report_hours('202429', 8)
    if response.status_code == 200:
        logger.info('Hours reported successfully. Please verify')


if __name__ == "__main__":
    main()
