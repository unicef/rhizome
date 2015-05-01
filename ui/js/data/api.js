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

function endPoint(path, mode) {
	mode = (mode) ? mode.toUpperCase() : 'GET';

	var defaults = {
		offset     : 0,
		format     : 'json',
		uri_display: 'id'
	};


	function fetch(query) {

		var req = prefix(request(mode, path));

		// form GET request
		if (mode === 'GET') {
			var q = _.defaults({}, query, defaults);
			req.query(q);
		}
		// form POST request
		else if (mode === 'POST') {
			req.query(defaults)
				.send(query);
		}

		return new Promise(function (fulfill, reject) {
			req.end(function (res) {
					if (res.error) {
						reject({
							status: res.status,
							msg: res.body.error
						});
					} else {
						fulfill({
							meta: res.body.meta || {},
							// FIXME: Checking for res.body.data because the campaign API
							// changed its response format so it no longer includes an
							// 'objects' property. This should only be a temporary workaround
							objects: res.body.objects || res.body.data || _.omit(res.body, 'meta')
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

		fetch(q).then(function (data) {
			var campaigns = data.objects.map(function (d) { return d.campaign; });

			endPoint('/campaign/')({
				id__in: campaigns
			}).then(function (campaignData) {
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
	campaign       : endPoint('/campaign/'),
	datapoints     : datapoint,
	datapointsRaw  : endPoint('/datapointentry/'),
	datapointUpsert: endPoint('/datapointentry/', 'post'),
	geo            : endPoint('/geo/'),
	indicators     : endPoint('/indicator/'),
	office         : endPoint('/office/'),
	regions        : endPoint('/region/')
};
