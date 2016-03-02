export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'builtin': true,
  'charts': [
    {
      'title': 'tableData',
      'type': 'TableChart',
      // 'location_ids': [1, 2],
      // 'locations': 'sublocations',
      'startDate': '2016-01-01',
      'endDate': '2016-01-01',
      'indicators': [27],
      'indicator_ids': [27],
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
