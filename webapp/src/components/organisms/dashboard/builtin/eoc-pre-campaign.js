export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'dashboardType': 'EocCampaign',
  'builtin': true,
  'charts': [
    {
      'title': 'tableData',
      'type': 'TableChart',
      'indicators': [1, 28, 12, 35, 2, 5, 27, 26, 13, 25, 19, 23, 7],
      'groupBy': 'indicator',
      'timeRange': {
        months: 0
      }
      // 'yFormat': ',.0f',
      // 'xFormat': ',.0f'
    }, {
      'title': 'trendData',
      'type': 'LineChart',
      'locations': 'sublocations',
      'groupBy': 'location',
      'indicators': [1],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'mapData',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [1]
    }
  ]
}
