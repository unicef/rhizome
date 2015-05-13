/* jshint browser: true */
/* global Promise */
'use strict';

var BASE_URL = '/api';

var _        = require('lodash');
var request  = require('superagent');
var prefix   = require('superagent-prefix')(BASE_URL);

var campaign = require('../data/model/campaign');

function urlencode(query) {
	return '?' + _.map(query, function (v, k) {
		return encodeURIComponent(k) + '=' + encodeURIComponent(v);
	}).join('&');
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];//jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function endPoint(path, mode, defaultVersion, useDefaults) {
	mode = (mode) ? mode.toUpperCase() : 'GET';
	defaultVersion = defaultVersion || 1;
	useDefaults = _.isUndefined(useDefaults) ? true : useDefaults;

	var defaults = {
		offset     : 0,
		format     : 'json',
		uri_display: 'id'
	};


	function fetch(query, version) {
		version = version || defaultVersion;

		var versionedPath = '/v' + version + path;
		var req = prefix(request(mode, versionedPath));

		// form GET request
		if (mode === 'GET') {
			var q = useDefaults ? _.defaults({}, query, defaults) : query;
			req.query(q);
		}
		// form POST request
		else if (mode === 'POST') {
		    var csrftoken = getCookie('csrftoken');
			req.query(defaults)
			    .set('X-CSRFToken',csrftoken)
			    .set('Content-Type','application/x-www-form-urlencoded')
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
							meta    : res.body.meta || {},
							objects : _.isArray(res.body) ?
								res.body :
								res.body.objects || _.omit(res.body, 'meta')
						});
					}
				});
		});
	}

	fetch.toString = function (query) {
		return BASE_URL + versionedPath + urlencode(_.defaults({}, query, defaults));
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
	regions        : endPoint('/region/'),
	document_review: endPoint('/source_data/document_review/'),
	map_field      : endPoint('/api_map_meta/','post'),

	admin: {
		usersMetadata: endPoint('/user/metadata/', 'get', 2, false),
		users: endPoint('/user/', 'get', 2, false)
	}
};
