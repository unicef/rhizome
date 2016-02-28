export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'builtin': true,
  'charts': [
    {
      'title': 'Polio Cases YTD',
      'section': 'impact',
      'indicators': [168],
      'startOf': 'year',
      'timeRange': {
        years: 2
      }
    }, {
      'title': 'Missed Children',
      'section': 'performance',
      'indicators': [166, 164, 167, 165],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'Missed Children by Province',
      'section': 'performance',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [475]
    }
  ]
}
