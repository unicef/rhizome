module.exports = {
	'title' : 'Test',
	'charts' : [{
			'title'      : 'Under-Immunized Children',
      'type'       : 'LineChart',
			'indicators' : [431,432,433],
      'series'     : 'indicator.short_name',
			'timeRange'  : {
				years : 3
			}
		}, {
			'title'      : 'Missed Children by Province',
      'type'       : 'ChoroplethMap',
      'region'     : 'subregions',
			'indicators' : [475],
		}, {
			'title'      : 'Conversions',
      'type'       : 'ScatterChart',
			'indicators' : [187,189],
      'timeRange'  : 0,
      'region'     : 'subregions'
		}
	]
};
