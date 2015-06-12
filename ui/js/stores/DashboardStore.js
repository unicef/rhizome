'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var moment = require('moment');

var api           = require('data/api');

var DashboardStore = Reflux.createStore({

	listenables : [require('actions/DashboardActions')],

	init : function () {
		this.loaded = false;
		this.indicators = {};

		Promise.all([api.dashboards(), api.regions(), api.campaign()])
			.then(function (responses) {
				var dashboards = responses[0].objects;

				this.regions    = responses[1].objects;
				this.campaigns  = responses[2].objects;
				this.dashboards = _.indexBy(dashboards, function (d) {
					return _.kebabCase(d.title);
				});

				this.loaded = true;

				this.onSetDashboard({
					dashboard : this.dashboard || _.kebabCase(dashboards[0].title)
				});
			}.bind(this));
	},

	getQueries : function () {
		var indicators = this.indicators;
		var qs = {};

		_.each(indicators, function (indicator, duration) {
			var s = String(duration);

			if (!qs.hasOwnProperty(s)) {
				qs[s] = [];
			}

			qs[s].push(indicator);
		});

		return _.map(qs, function (duration, indicators) {
			return {
				indicators : indicators,
				duration   : moment.duration(duration)
			}
		});
	},

	onSetDashboard : function (definition) {
		this.dashboard = definition.dashboard;
		this.region    = definition.region || this.region;
		this.date      = definition.date || this.date;

		if (!this.loaded) {
			return;
		}

		var dashboard = this.dashboards[this.dashboard];

		_.each(dashboard.charts, this.addChartDefinition);

		var regions   = this.regions;
		var campaigns = this.campaigns;

		var regionIdx       = _.indexBy(regions, 'id');
		var topLevelRegions = _(regions)
			.filter(function (r) {
				return !regionIdx.hasOwnProperty(r.parent_region_id);
			})
			.sortBy('name');

		var region = _.find(regions, function (r) {
				return r.name === this.region;
			}.bind(this));

		if (_.isFinite(dashboard.default_office_id) && _.get(region, 'office_id') !== dashboard.default_office_id) {
			region = topLevelRegions.find(function (r) {
				return r.office_id === dashboard.default_office_id;
			});
		}

		if (!region) {
			region = topLevelRegions.first();
		}

		var campaign = _(campaigns)
				.filter(function (c) {
					return c.office_id === region.office_id &&
					(!this.date || _.startsWith(c.start_date, this.date));
				}.bind(this))
				.sortBy('start_date')
				.last();

		this.trigger({
			dashboard : dashboard,
			region    : region,
			campaign  : campaign,

			regions   : regions,
			campaigns : _.filter(campaigns, function (c) {
				return c.office_id === region.office_id;
			})
		});
	},

	addChartDefinition : function (chart) {
		_.each(chart.indicators, function (id) {
			var duration = moment.duration(chart.timeRange);

			if (!this.indicators.hasOwnProperty(id) || duration > this.indicators[id]) {
				this.indicators[id] = duration;
			}
		}.bind(this));
	}
});

module.exports = DashboardStore;
