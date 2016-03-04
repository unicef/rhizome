export default {
  'id': -9,
  'title': 'EOC Pre Campaign',
  'dashboardType': 'EocCampaign',
  'builtin': true,
  'charts': [
    {
      'title': 'tableData',
      'type': 'TableChart',
      'indicators': [2, 5, 6, 11, 12, 18, 22, 24, 25, 26, 28, 1],
      'groupBy': 'indicator',
      'timeRange': {
        months: 0
      }
      // 'yFormat': ',.0f',
      // 'xFormat': ',.0f'
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
