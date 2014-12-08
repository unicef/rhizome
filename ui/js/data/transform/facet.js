var _ = require('lodash');

module.exports = function facet(name, get) {
	'use strict';

	if (typeof get !== 'function') {
		get = function (o) {
			return o[get];
		};
	}

	function transform(data) {
		return _.map(_.groupBy(data, get), function (points, facet) {
			var o = {
				'points': points
			};

			o[name] = facet;

			return o;
		});
	}

	return transform;
};
