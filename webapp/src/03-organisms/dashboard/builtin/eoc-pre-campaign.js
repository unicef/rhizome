export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'builtin': true,
  'charts': [
    {
      'type': 'TableChart',
      'location_ids': [33,424,1,432,428,429,40,37,351,431,47,50,422,415,45,414,420,426],
      'startDate': '2015-01-01',
      'endDate': '2016-01-01',
      'indicators': [20, 21],
      'indicator_ids': [20, 21],
      'yFormat': ',.0f',
      'groupBy': 'indicator',
      'xFormat': ',.0f'
    }, {
      'title': 'trendData',
      'type': 'LineChart',
      'indicators': [21],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'mapData',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [21]
    }
  ]
}
