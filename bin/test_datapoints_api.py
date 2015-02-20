#!/usr/bin/env python

import csv
import json
import psycopg2
import time
import urllib2

from datetime import datetime
from urllib import urlencode


class Record:
    @classmethod
    def connect(cls, host, user, password, database):
        cls.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    @classmethod
    def disconnect(cls):
        cls.connection.close()

    def __hash__(self):
        return self.id


class Campaign(Record):
    class NotFoundError(LookupError):
        pass

    __slots__ = ['id', 'office', 'date']

    _campaigns = {}

    @classmethod
    def get(cls, name):
        if name not in cls._campaigns:

            try:
                office, month, year = name.split()
            except ValueError:
                cls._campaigns[name] = None
            else:
                start = datetime.strptime(' '.join([month, year]), '%B %Y').strftime('%Y-%m-%d')

                c = cls.connection.cursor()
                c.execute('''SELECT c.id
                    FROM campaign AS c
                    JOIN office AS o ON o.id = c.office_id
                    WHERE o.name = %s AND c.start_date = %s;''',
                    (office, start))

                try:
                    cls._campaigns[name] = Campaign(c.fetchone()[0], office, '{} {}'.format(month, year))
                except (TypeError, IndexError):
                    cls._campaigns[name] = None
                finally:
                    c.close()

        if not cls._campaigns[name]:
            raise Campaign.NotFoundError

        return cls._campaigns[name]

    def __init__(self, id, office, date):
        self.id = id
        self.office = office
        self.date = date

    def __hash__(self):
        return self.id

    def __str__(self):
        return '{} {} ({})'.format(self.office, self.date, self.id)


class Region(Record):
    class NotFoundError(LookupError):
        pass

    __slots__ = ['id', 'name']

    _regions = {}

    @classmethod
    def get(cls, name):
        if name not in cls._regions:
            c = cls.connection.cursor()
            c.execute('''SELECT id
                FROM region
                WHERE name = %s''', (name, ))

            try:
                cls._regions[name] = Region(c.fetchone()[0], name)
            except (TypeError, IndexError):
                cls._regions[name] = None
            finally:
                c.close()

        if not cls._regions[name]:
            raise Region.NotFoundError

        return cls._regions[name]

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class Indicator(Record):
    __slots__ = ['id', 'name']

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class MultipleValuesError(Exception):
    pass


class DataPoint:
    auth = {
        'username': 'evan',
        'api_key': '67bd6ab9a494e744a213de2641def88163652dad'
    }

    @classmethod
    def connect(cls, host):
        cls.url = 'http://' + host + '/api/v1/datapoint/'

        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, host, 'unicef', 'stoppolio')
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)

        cls.opener = urllib2.build_opener(handler)

    def __init__(self, campaign, region, indicator):
        response = self.opener.open(self.url + '?' + urlencode(dict(
            campaign__in=campaign,
            region__in=region,
            indicator__in=indicator,
            **self.auth
        )))

        objects = json.loads(response.read())['objects']

        if len(objects) > 1:
            raise MultipleValuesError

        try:
            for datum in objects[0]['indicators']:
                if datum['indicator'] == indicator:
                    self.value = datum['value']
        except IndexError:
            self.value = None


class Summary:
    def __init__(self):
        self.total = 0
        self.results = {}

    def add(self, result):
        self.total += 1
        self.results[result.type] = self.results.get(result.type, 0) + 1

    def __iter__(self):
        for result_type, count in self.results.iteritems():
            yield (result_type, count, float(count) / self.total)

        yield ('Total', self.total)


class Result:
    fields = [
        'Type',
        'Campaign',
        'Campaign ID',
        'Region',
        'Region ID',
        'Indicator',
        'Indicator ID',
        'Expected',
        'Actual'
    ]

    type = ''

    def __init__(self, campaign, region, indicator, expected=None, actual=None):
        self.campaign = campaign
        self.region = region
        self.indicator = indicator
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return '{}: {} {} {} expected {}, found {}'.format(
            self.type,
            self.campaign,
            self.region,
            self.indicator,
            self.expected,
            self.actual
        )

    def toDict(self):
        return {
            'Type': self.type,
            'Campaign': '{} {}'.format(self.campaign.office, self.campaign.date),
            'Campaign ID': self.campaign.id,
            'Region': self.region.name,
            'Region ID': self.region.id,
            'Indicator': self.indicator.name,
            'Indicator ID': self.indicator.id,
            'Expected': self.expected,
            'Actual': self.actual
        }


class Success(Result):
    type = 'Success'


class Failure(Result):
    type = 'Failure'


class CampaignNotFound(Failure):
    type = 'Campaign Not Found'

    def __init__(self, campaign):
        self.campaign = campaign

    def __str__(self):
        return '{}: {}'.format(self.type, self.campaign)

    def toDict(self):
        return {
            'Type': self.type,
            'Campaign': self.campaign
        }


class RegionNotFound(Failure):
    type = 'Region Not Found'

    def __init__(self, region):
        self.region = region

    def __str__(self):
        return '{}: {}'.format(self.type, self.region)

    def toDict(self):
        return {
            'Type': self.type,
            'Region': self.region
        }


class MultipleValues(Failure):
    type = 'Too Many Values'


class MissingValue(Failure):
    type = 'Missing Value'


class UnexpectedValue(Failure):
    type = 'Unexpected Value'


class IncorrectValue(Failure):
    type = 'Incorrect Value'


def init():
    parser = argparse.ArgumentParser(description='Test Polio backend API')

    # Database options
    parser.add_argument('--host', default='50.57.77.252',
        help='Hostname or IP for database connection')
    parser.add_argument('-u', '--user', default='djangoapp',
        help='Username for database connection')
    parser.add_argument('-d', '--db', default='polio',
        help='The database name to connect to')

    # Test options
    parser.add_argument('-t', '--threshold', default=0.0000001, type=float,
        help='Values whose difference is greater than this threshold will be considered failed tests')
    parser.add_argument('-a', '--api', default='uf04.seedscientific.com',
        help='Domain for API')

    # Output options
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
        help='Output file to store results')
    parser.add_argument('-v', '--verbose', action='store_true',
        help='Include successful tests in output as well as failures')

    # Inputs
    parser.add_argument('cases', metavar='TESTS.CSV', type=argparse.FileType('rU'),
        help='CSV containing test caseDef definitions')

    args = parser.parse_args()

    args.password = getpass.getpass('Password {}@{}:'.format(args.user, args.host))


    return args


def test(campaign_id, region_id, indicator_id, expected, threshold=0):
    try:
        actual = DataPoint(campaign_id, region_id, indicator_id)
    except MultipleValuesError:
        return MultipleValues(campaign_id, region_id, indicator_id)

    try:
        if abs(float(expected) - actual.value) > threshold:
            return IncorrectValue(campaign_id, region_id, indicator_id, expected, actual.value)
    except ValueError:
        if expected in ('', '#DIV/0!'):
            if actual.value:
                return UnexpectedValue(campaign_id, region_id, indicator_id, actual.value)
        else:
            raise
    except TypeError:
        if expected not in ('', '#DIV/0!'):
            return MissingValue(campaign_id, region_id, indicator_id, expected)

    return Success(campaign_id, region_id, indicator_id, expected, actual.value)


def runTests(cases):
    results = []

    for caseDef in cases:
        try:
            print caseDef
            yield test(
                caseDef['campaign_id'],
                caseDef['region_id'],
                caseDef['indicator_id'],
                caseDef['value'],
                # args.threshold
            )
        except Campaign.NotFoundError:
            yield CampaignNotFound(caseDef['Campaign'])
        except Region.NotFoundError:
            yield RegionNotFound(caseDef['Region'])


if __name__ == '__main__':
    import argparse
    import getpass

    args = init()

    Record.connect(args.host, args.user, args.password, args.db)

    DataPoint.connect(args.api)

    summary = Summary()

    writer = None
    if args.output:
        writer = csv.DictWriter(args.output, Result.fields)
        writer.writeheader()

    start = time.clock()
    for result in runTests(csv.DictReader(args.cases)):

        print 1
    #     if args.verbose or isinstance(result, Failure):
    #         print result
    #
    #     if writer:
    #         writer.writerow(result.toDict())
    #
    #     summary.add(result)

    end = time.clock()
    Record.disconnect()

    print
    for result in summary:
        if len(result) > 2:
            print '{}: {} ({:.1%})'.format(*result)
        else:
            print '{}: {}'.format(*result)

    print
    print 'Elapsed time:', end - start
