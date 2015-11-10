module.exports = {
    'id': -7,
    'title': 'Homepage Pakistan',
  'builtin': true,
    'charts': [{
            'title': 'Polio Cases YTD',
            'section': 'impact',
            'indicators': [168],
            'startOf': 'year',
            'timeRange': {
                years: 2
            }
        }, {
            'title': 'Under-Immunized Children',
            'section': 'impact',
            'indicators': [431, 432, 433],
            'startOf': 'quarter',
            'timeRange': {
                years: 3
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
