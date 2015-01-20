/* global Promise */
'use strict';

var BASE_URL = '/api/v1';

var _        = require('lodash');
var request  = require('superagent');
var prefix   = require('superagent-prefix')(BASE_URL);

var campaign = require('../data/model/campaign');

function urlencode(query) {
	return '?' + _.map(query, function (v, k) {
		return encodeURIComponent(k) + '=' + encodeURIComponent(v);
	}).join('&');
}

function endPoint(path) {
	var defaults = {
		offset     : 0,
		username   : 'evan',
		api_key    : '67bd6ab9a494e744a213de2641def88163652dad',
		format     : 'json',
		uri_display: 'id'
	};


	function fetch(query) {
		var q = _.defaults({}, query, defaults);

		return new Promise(function (fulfill, reject) {
			prefix(request.get(path))
				.query(q)
				.end(function (res) {
					if (res.error) {
						reject({
							status: res.status,
							msg: res.body.error
						});
					} else {

						fulfill({
							meta: res.body.meta || {},
							objects: res.body.objects || _.omit(res.body, 'meta')
						});
					}
				});
		});
	}

	fetch.toString = function (query) {
		return BASE_URL + path + urlencode(_.defaults({}, query, defaults));
	};

	return fetch;
}

function datapoint(q) {
	var fetch = endPoint('/datapoint/');

	// Return a promise so we can chain the requests for datapoints with the
	// campaign lookups.
	return new Promise(function (fulfill, reject) {

		// Fetch datapoints first, then look up the campaigns. Once campaign data
		// has been filled in, fulfill the promise.

		fetch(q).done(function (data) {
			var campaigns = data.objects.map(function (d) { return d.campaign; });

			endPoint('/campaign/')({
				id__in: campaigns
			}).done(function (campaignData) {
				var campaigns = _.indexBy(campaignData.objects, 'id');

				// Replace the campaign IDs with campaign objects
				for (var i = data.objects.length - 1; i >= 0; --i) {
					data.objects[i].campaign = campaign(campaigns[data.objects[i].campaign]);
				}

				fulfill(data);
			});

		}, reject);

	});
}

datapoint.toString = function (query) {
	return endPoint('/datapoint/').toString(query);
};

module.exports = {
	campaign  : endPoint('/campaign/'),
	indicators: endPoint('/indicator/'),
	regions   : endPoint('/region/'),
	datapoints: datapoint,
	datapointsRaw: endPoint('/datapointentry/'),
	office    : endPoint('/office/')
};
