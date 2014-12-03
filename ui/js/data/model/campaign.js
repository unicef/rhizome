var _      = require('lodash');
var moment = require('moment');
var api    = require('../api');

function update(campaign, obj) {
	'use strict';

	_.assign(campaign, _.omit(obj, 'created_at', 'start_date', 'end_date'));

	campaign.created_at = moment(obj.created_at);
	campaign.start_date = moment(obj.start_date, 'YYYY-MM-DD');
	campaign.end_date   = moment(obj.end_date, 'YYYY-MM-DD');
}

function Campaign(obj) {
	'use strict';

	if (!(this instanceof Campaign)) {
		return new Campaign(obj);
	}

	if (obj) {
		update(this, obj);
	} else {
		_.extend(this, {
			id          : null,
			created_at  : null,
			start_date  : null,
			end_date    : null,
			name        : null,
			slug        : null,
			resource_uri: null
		});
	}
}

Campaign.fetch = function (id) {
	'use strict';

	var campaign = new Campaign();

	api.campaign({
		id: id
	}).done(function (data) {
		update(campaign, data);
	});

	return campaign;
};

module.exports = Campaign;
