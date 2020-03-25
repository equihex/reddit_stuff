import praw
import datetime
from dateutil.relativedelta import *

class SotdPostLocator(object):
    """
    Get
    """

    THREAD_NAME_STR_PATTERN = ' SOTD Thread -'

    def __init__(self, praw):
        self.praw = praw

    @property
    def last_month(self):
        return datetime.date.today() - relativedelta(months=2)

    def get_x_most_recent_threads(self, threads_to_fetch=50):
        res = self.praw.subreddit('wetshaving').search(
            query='"*SOTD Thread -"',
            limit=threads_to_fetch,
        )
        return [x for x in res if self.THREAD_NAME_STR_PATTERN in x.title]

    def get_threads_from_last_month(self):
        """
        Return list of threads from previous month
        :return:
        """
        rec = self.get_x_most_recent_threads(120)
        return [x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == self.last_month.month]

    def get_threads_for_given_month(self, given_month):
        """
        Return list of threads from previous month
        :return:
        """
        if not isinstance(given_month, datetime.date):
            raise AttributeError('Must pass in a datetime.date object')

        rec = self.praw.subreddit('wetshaving').search(
            query='SOTD Thread {0} {1}'.format(given_month.strftime('%b'), given_month.year),
            limit=100,
        )

        return [x for x in rec if datetime.datetime.utcfromtimestamp(x.created_utc).month == given_month.month]

    def process(self):
        threads = self.get_x_most_recent_threads(50)
        orderable = {x.created_utc: x.title for x in threads}

        for sotd_date in sorted(orderable.keys()):
            print(sotd_date, orderable[sotd_date])



if __name__ == '__main__':
    # debug / testing
    pl = SotdPostLocator(praw.Reddit('standard_creds', user_agent='arach'))

    res = pl.praw.subreddit('wetshaving').search(
        query='SOTD Thread Aug 2019',
        limit=1000,

    )
    # res = pl.get_threads_from_last_month()
    orderable = {x.created_utc: x.title for x in res}

    for sotd_date in sorted(orderable.keys()):
        print(sotd_date, orderable[sotd_date])