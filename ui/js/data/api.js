/* global Promise */
'use strict';

var _ = require('lodash');
var request = require('superagent');
var prefix = require('superagent-prefix')('/api/v1');

function fetch(path, query) {

	var fetchAll = (!query.limit || query.limit < 1),
		accumulator = { objects: [] },
		q = _.defaults({}, query, {
			offset: 0,
			username: 'evan',
			api_key: '67bd6ab9a494e744a213de2641def88163652dad',
			format: 'json'
		}),
		p = new Promise(function (fulfill) {
			function get() {
				prefix(request.get(path))
					.query(q)
					.end(got);
			}

			function got(res) {
				accumulator.meta = res.body.meta;
				accumulator.objects = accumulator.objects.concat(res.body.objects);

				if (fetchAll && res.body.meta.next) {
					q.offset += res.body.meta.limit;
					get();
				} else {
					fulfill(accumulator);
				}
			}

			get();
		});

	return p;
}

function encodeArray(a) {
	if (!(a instanceof Array)) {
		return String(a);
	}

	return a.join(',');
}

module.exports = {
	campaign: function (query) {
		var q = _.defaults({}, query, {
			limit: 0
		});

		return fetch('/campaign/', q);
	},
	indicators: function (query) {
		var q = _.defaults({}, query, {
			limit: 0
		});

		return fetch('/indicator/', q);
	},
	regions: function (query) {
		var q = _.defaults({}, query, {
			limit: 0
		});

		return fetch('/region/', q);
	},
	datapoints: function (query) {
		var q = _.defaults(_.omit(query, 'indicators', 'regions'), {
				limit: 20
			});

		if (query.indicators && query.indicators.length) {
			q.indicator__in = encodeArray(query.indicators);
		}

		if (query.regions && query.regions.length) {
			q.region__in = encodeArray(query.regions);
		}

		// This is ugly...
		return fetch('/datapoint/', q).then(function (res) {
			// Group each data point by its campaign and region
			var grouped = _.groupBy(res.objects, function (d) {
				return [d.campaign, d.region];
			});

			var values = _.values(grouped);

			// Map-reduce!
			var rows = values.map(function (arr) {
				return _.reduce(arr, function (result, d) {
					_.defaults(result, _.pick(d, 'campaign', 'region'));

					result[d.indicator] = d.value;
					return result;
				}, {});
			});

			return {
				meta: res.meta,
				objects: rows
			};
		});
	}
};
