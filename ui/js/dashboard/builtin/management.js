module.exports = {
	'id'   : 1,
	'title' : 'Management Dashboard',
	'charts' : [{
			'title'      : 'Polio Cases YTD',
			'section'    : 'impact',
			'indicators' : [168],
			'startOf'    : 'year',
			'timeRange'  : {
				years : 2
			},
		}, {
			'title'      : 'Under-Immunized Children',
			'section'    : 'impact',
			'indicators' : [431,432,433],
			'startOf'    : 'quarter',
			'timeRange'  : {
				years : 3
			}
		}, {
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
      'region'     : 'subregions',
			'indicators' : [475],
		}, {
			'title'      : 'Conversions',
			'section'    : 'performance',
			'indicators' : [187,189],
			'timeRange'  : {
				months : 12
			}
		}, {
			'title'      : 'Microplans',
			'section'    : 'performance',
			'indicators' : [27,28],
		}, {
			'title'      : 'Transit Points',
			'section'    : 'performance',
			'indicators' : [175,176,177,204],
		}, {
			'title'      : 'FLW\'s Capacity to Perform',
			'indicators' : [178,228,179,184,180,185,230,226,239],
			'timeRange'  : {
				months : 4
			}
		}, {
			'title'      : 'Polio+',
			'indicators' : [245,236,192,193,191],
			'timeRange'  : {
				months : 4
			}
		}, {
			'title'      : 'Supply',
			'indicators' : [194,219,173,172],
			'timeRange'  : {
				months : 4
			}
		}, {
			'title'      : 'Resources',
			'indicators' : [169,233],
			'timeRange'  : {
				months : 4
			}
		}, {
			'title'      : 'Number of Inaccessible Children',
			'section'    : 'access',
			'indicators' : [158],
			'timeRange'  : {
				months : 12
			}
		}, {
			'title'      : 'Districts with Access Plans',
			'section'    : 'access',
			'indicators' : [174],
		}, {
			'title'      : 'Inaccessibility Breakdown',
			'section'    : 'access',
			'indicators' : [442,443,444,445,446,447,448,449,450]
		}
	]
};
