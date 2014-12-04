'use strict';
var _ = require('lodash');

module.exports = function bullet(name, numerator, denominator, ranges) {

	function model(data) {
		var obj;
		var whole = 0;
		var part  = 0;

		for (var i = data.objects.length - 1; i >= 0; i--) {
			var d          = data.objects[i];
			var indicators = _.indexBy(d.indicators, 'indicator');
			var w          = Number(indicators[denominator].value);
			var p          = Number(indicators[numerator].value);

			if (!obj || d.campaign.start_date > obj.campaign.start_date) {
				obj = d;
				obj.value = (w > 0) ? p / w : null;
			}

			whole += w;
			part  += p;
		}

		return _.assign(obj, {
			title : name,
			marker: part / whole,
			ranges: ranges
		});
	}

	return model;
};
