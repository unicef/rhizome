/* jshint browser: true */
/* global Promise */
'use strict';

var BASE_URL = '/api';

var _        = require('lodash');
var request  = require('superagent');
var prefix   = require('superagent-prefix')(BASE_URL);

var treeify = require('../data/transform/treeify');
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

	fetch.toString = function (query, version) {
		version = version || defaultVersion;
		var versionedPath = '/v' + version + path;

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

			endPoint('/campaign/', 'get', 2)({
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
datapoint.toString = function (query, version) {
	return endPoint('/datapoint/').toString(query, version);
};

function indicatorsTree(q) {
	var fetch1 = endPoint('/indicator/', 'get', 2);
	var fetch2 = endPoint('/indicator_tag', 'get', 2);
	var makeTagId = function(tId) { return 'tag-'+tId; };
	return new Promise(function (fulfill, reject) {

		fetch1(q).then(function (indicators) {
			fetch2().then(function(tags) {
				var tags_map = {};
				_.each(tags.objects, function(t) {
							tags_map[t.id] = t;
							t.id = makeTagId(t.id);
							t.noValue = true;
							t.parent = t.parent_tag_id && t.parent_tag_id !== 'None' ? makeTagId(t.parent_tag_id) : null;
							t.children = [];
							t.title = t.tag_name;
							t.value = t.id;
						});

				// add 'Other Indicators' tag to collect any indicators without tags
				var otherTag = {
					'id': 0,
					'value': makeTagId(0),
					'noValue': true,
					'title': 'Other Indicators',
					'children': []
				};
				
				_.each(indicators.objects, function(i) {
						i.title = i.name;
						i.value = i.id;
						if (!_.isArray(i.tag_json) || i.tag_json.length === 0) {
							otherTag.children.push(i);
						}
						else if (_.isArray(i.tag_json)) {
							_.each(i.tag_json, function(tId) {
								tags_map[tId].children.push(i);
							});
						}
					});

				// add other tag?
				if (otherTag.children.length > 0) {
					tags.objects.push(otherTag);
				}

				// sort indicators with each tag
				_.each(tags.objects, function(t) {
					t.children = _.sortBy(t.children, 'title');
				});

				tags.objects = treeify(tags.objects, 'id');
				tags.flat = indicators.objects;
				fulfill(tags);
			});
		}, reject);
	});
}	

module.exports = {
	campaign              : endPoint('/campaign/', 'get', 2),
	dashboards            : function () {
		// FIXME: temporary mock data
		return Promise.resolve({ objects : [] });
	},
	dashboardsCustom      : endPoint('/custom_dashboard/', 'get', 2),
	datapoints            : datapoint,
	datapointsRaw         : endPoint('/datapointentry/'),
	datapointUpsert       : endPoint('/datapointentry/', 'post'),
	document              : endPoint('/document/', 'get', 2),
	geo                   : endPoint('/geo/'),
	indicators            : endPoint('/indicator/', 'get', 2),
	indicatorsTree		  : indicatorsTree,
	office                : endPoint('/office/', 'get', 2),
	regions               : endPoint('/region/', 'get', 2),
	document_review       : endPoint('/document_review/','get',2),
	//map_field             : endPoint('/api_map_meta/','post',2),
	map_indicator         : endPoint('/indicator_map/','post',2),
	map_region            : endPoint('/region_map/','post',2),
	map_campaign          : endPoint('/campaign_map/','post',2),
	user_permissions      : endPoint('/user_permission/', 'get', 2),
	groups                : endPoint('/group/','get',2),
	groupUpsert           : endPoint('/group/', 'post', 2),
	user_groups           : endPoint('/user_group/','get',2),
	group_permissions     : endPoint('/group_permission/','get',2),
	group_permissionUpsert: endPoint('/group_permission/', 'post', 2),
	map_user_group        : endPoint('/user_group/','post',2),
	region_permission     : endPoint('/region_permission/','get',2),
	set_region_permission : endPoint('/region_permission/','post',2),
	admin: {
		usersMetadata: endPoint('/user/metadata/', 'get', 2, false),
		users: endPoint('/user/', 'get', 2, false),
		groupsMetadata: endPoint('/group/metadata/', 'get', 2, false),
		groups: endPoint('/group/', 'get', 2, false),
		regionsMetadata: endPoint('/region/metadata/', 'get', 2, false),
		regions: endPoint('/region/', 'get', 2, false),
		campaignsMetadata: endPoint('/campaign/metadata/', 'get', 2, false),
		campaigns: endPoint('/campaign/', 'get', 2, false),
		indicatorsMetadata: endPoint('/indicator/metadata/', 'get', 2, false),
		indicators: endPoint('/indicator/', 'get', 2, false),
	}
};
