"""Timezone module."""

from datetime import datetime
from datetime import timezone as d_timezone

import zoneinfo

from src.config import settings


class TimeZone:
    """_summary_."""

    def __init__(self, tz: str = settings.DATETIME_TIMEZONE):
        """_summary_.

        Args:
            tz (str, optional): _description_. Defaults to settings.DATETIME_TIMEZONE.
        """
        self.tz_info = zoneinfo.ZoneInfo(tz)

    def now(self) -> datetime:
        """Get current local time.

        Returns:
            datetime: _description_
        """
        return datetime.now(self.tz_info)

    def now_utc(self) -> datetime:
        """Get current UTC time.

        Returns:
            datetime: _description_
        """
        return datetime.now(d_timezone.utc)

    def f_datetime(self, dt: datetime) -> datetime:
        """Datetime to timezone.

        Args:
            dt (datetime): _description_

        Returns:
            datetime: _description_
        """
        return dt.astimezone(self.tz_info)

    def f_str(
        self, date_str: str, format_str: str = settings.DATETIME_FORMAT
    ) -> datetime:
        """Time string to time zone time.

        Args:
            date_str (str): _description_
            format_str (str, optional): _description_. Defaults to settings.DATETIME_FORMAT.

        Returns:
            datetime: _description_
        """
        return datetime.strptime(date_str, format_str).replace(
            tzinfo=self.tz_info
        )


timezone = TimeZone()
