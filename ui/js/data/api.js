/* global Promise */
'use strict';

var BASE_URL = '/api/v1';
var _ = require('lodash');
var request = require('superagent');
var prefix = require('superagent-prefix')(BASE_URL);

function urlencode(query) {
	return '?' + _.map(query, function (v, k) {
		return encodeURIComponent(k) + '=' + encodeURIComponent(v);
	}).join('&');
}

function endPoint(path) {
	var defaults = {
		offset: 0,
		username: 'evan',
		api_key: '67bd6ab9a494e744a213de2641def88163652dad',
		format: 'json'
	};


	function fetch(query) {
		var q = _.defaults({}, query, defaults);

		return new Promise(function (fulfill) {
			prefix(request.get(path))
				.query(q)
				.end(function (res) {
					fulfill({
						meta: res.body.meta || {},
						objects: res.body.objects || _.omit(res.body, 'meta')
					});
				});
		});
	}

	fetch.toString = function (query) {
		return BASE_URL + path + urlencode(_.defaults({}, query, defaults));
	};

	return fetch;
}

module.exports = {
	campaign: endPoint('/campaign/'),
	indicators: endPoint('/indicator/'),
	regions: endPoint('/region/'),
	datapoints: endPoint('/datapoint/')
};
