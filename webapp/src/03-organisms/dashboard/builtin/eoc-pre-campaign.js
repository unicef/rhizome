export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'builtin': true,
  'charts': [
    {
      'title': 'tableData',
      'type': 'TableChart',
      'indicators': [21, 20],
      'startOf': 'year',
      'timeRange': {
        years: 2
      }
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
