import requests
import logging
from bs4 import BeautifulSoup
from .settings import PxSettings


logger = logging.getLogger(__name__)

class PxClient:
    def __init__(self, settings: PxSettings):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0"
        self.session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"

        self.settings = settings

    def login(self):
        logger.debug(f"logging in to {self.settings.base_url} with {self.settings.username} and {self.settings.password}")
        self.session.post(
            f"{self.settings.base_url}/login/check_login.asp",
            data={
                "hdnsettings": "100,0",
                "username": self.settings.username,
                "password": self.settings.password,
                "server": self.settings.server,
                "database": self.settings.database,
                "selectLanguage": "SWE"
            }
        )
        return AuthorizedClient(self.settings, self.session)

class AuthorizedClient:
    def __init__(self, settings: PxSettings, session: requests.Session):
        logger.debug('creating authorized client with cookies')
        self.settings = settings
        self.session = session
        self._initialize_frameset()

    def _initialize_frameset(self):
        # don't ask questions
        self.session.post(
            'https://px.sigmatechnology.se/timebase/frameset.asp',
            data={"initparam": "1",}
        )

    def _create_report(self, week: str):
        """ Create a new report for the given week. """

        # set_period is also used when modifying a report, but we dont care about that
        self.session.post(
            f"{self.settings.base_url}/timebase/time/set_period.asp",
            data={
                "userAction": "other",
                "otherPeriod": week,
                "copyAction": "blank",
            }
        )

    def _add_row(self):
        """ Add a new row with configured project and activity to the report. """
        self.session.post(
            f"{self.settings.base_url}/timebase/time/enter_row.asp",
            data={
                "activity": self.settings.activity,
                "project": self.settings.project,
                "current_row": "new"
            }
        )

    def _retrieve_report_days(self):
        """ 
        Retrieve the days of the week that we are expecting to report hours on.
        Must be called after _create_report since the API is stateful.
        """
        response = self.session.get(
            f"{self.settings.base_url}/timebase/time/report.asp?row=",
            headers={
                "User-Agent": "Mozilla/5.0",
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')

        # not sure if we need this yet, but this retrieves the days of the month
        # e.g. 17, 18, 19, 20, 21, 22, 23
        # number_els = soup.select(".headerfootergradientbottom th:has(font) div font")
        # numbers = [int(el.text) for el in number_els]

        day_els = soup.select(".headerfootergradienttop th:has(font)")
        # mask used to filter out weekend ("red") days that we don't want to report hours on
        mask = ["px-weekname-weekend" not in day["class"] for day in day_els]

        days_expecting_work_hours = []
        for i, ok_day in enumerate(mask):
            if ok_day:
                days_expecting_work_hours.append(i+1)
        return days_expecting_work_hours


    def report_hours(self, week: str, hours: int):
        self._create_report(week)
        days = self._retrieve_report_days()
        self._add_row()

        form_data = {}
        for day in days:
            form_data[f"day_1_{day}"] = f"{hours},0"

        response = self.session.post(
            f"{self.settings.base_url}/timebase/time/save_report.asp?dirty=1",
            data=form_data,
        )

        return response
