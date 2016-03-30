export default {
  'id': -10,
  'title': 'EOC Intra Campaign',
  'dashboardType': 'EocCampaign',
  'builtin': true,
  'charts': [
    {
      'title': 'tableData',
      'type': 'TableChart',
      'indicators': [4, 28, 9, 11, 20, 8, 10, 22, 24, 6],
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
      'indicators': [4],
      'timeRange': {
        months: 12
      }
    }, {
      'title': 'mapData',
      'type': 'ChoroplethMap',
      'locations': 'sublocations',
      'timeRange': 0,
      'indicators': [4]
    }
  ]
}
