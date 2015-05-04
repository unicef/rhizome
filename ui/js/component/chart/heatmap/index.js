'use strict';

var palette = require('util/colorbrewer');
var util    = require('util/data');

module.exports = {
	template : require('./template.html'),

	data : function () {
		return {
			columnLabels : [],
			series       : []
		};
	},

	filters : {
		color : function (value) {
			var p = palette.RdYlBu[11];
			var scale = d3.scale.quantile()
				.range(d3.range(p.length))
				.domain([0, 1]);

			return util.defined(value) ? p[scale(value)] : 'transparent';
		}
	}

};
