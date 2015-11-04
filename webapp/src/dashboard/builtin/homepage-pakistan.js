module.exports = {
	'id'   : -7,
	'title' : 'Homepage Pakistan',
  'builtin': true,
	'charts' : [{
			'title'      : 'Missed Children',
			'section'    : 'performance',
			'indicators' : [166,164,167,165],
			'timeRange'  : {
				months : 12
			}
		}, {
			'title'      : 'Missed Children by Province',
			'section'    : 'performance',
      'type'       : 'ChoroplethMap',
      'locations'  : 'sublocations',
      'timeRange'  : 0,
			'indicators' : [475]
		}, {
			'title'      : 'Conversions',
			'section'    : 'performance',
			'indicators' : [187,189],
			'timeRange'  : {
				months : 12
			}
		}
	]
};
