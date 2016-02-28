export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'builtin': true,
  'charts': [
    {
      'title': 'Polio Cases YTD',
      'type': 'LineChart',
      'indicators': [168],
      'startOf': 'year',
      'timeRange': {
        years: 2
      }
    }, {
      'title': 'Missed Children',
      'type': 'LineChart',
      'indicators': [475],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'Missed Children by Province',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [475]
    }
  ]
}
