export default {
  'id': -1,
  'title': 'Management Dashboard',
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
    }, {
      'title': 'Conversions',
      'section': 'performance',
      'indicators': [187, 189],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'Transit Points',
      'section': 'performance',
      'timeRange': 0,
      'indicators': [175, 176, 177, 204]
    }, {
      'title': 'FLW\'s Capacity to Perform',
      'indicators': [178, 179, 239, 184, 185, 226],
      'timeRange': {
        months: 4
      }
    }, {
      'title': 'Vaccinators',
      'indicators': [180, 230, 228],
      'timeRange': {
        months: 4
      }
    }, {
      'title': 'Supply',
      'indicators': [194, 219, 173, 172],
      'timeRange': {
        months: 4
      }
    }, {
      'title': 'Routine',
      'indicators': [245, 236],
      'timeRange': {
        months: 4
      }
    }, {
      'title': 'Resources',
      'indicators': [169, 233],
      'timeRange': {
        months: 4
      }
    }, {
      'title': 'Number of Inaccessible Children',
      'section': 'access',
      'indicators': [158],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'Districts with Access Plans',
      'section': 'access',
      'indicators': [174],
      'timeRange': 0
    }, {
      'title': 'Inaccessibility Breakdown',
      'section': 'access',
      'indicators': [442, 443, 444, 445, 446, 447, 448, 449, 450],
      'timeRange': 0
    }, {
      'title': 'Microplans',
      'indicators': [27, 28],
      'timeRange': 0
    }, {
      'title': 'Vaccinated Children by Province',
      'section': 'performance',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [177]
    }, {
      'title': 'Access Challenged District by Province',
      'section': 'performance',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [203]
    }
  ]
}
