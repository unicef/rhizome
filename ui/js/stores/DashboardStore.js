'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var moment = require('moment');

var api      = require('data/api');
var builtins = require('dashboard/builtin');

var DashboardStore = Reflux.createStore({

	listenables : [require('actions/DashboardActions')],

	init : function () {
		this.loaded = false;
		this.indicators = {};

		Promise.all([api.dashboards(), api.regions(), api.campaign()])
			.then(function (responses) {
				var dashboards = builtins.concat(responses[0].objects);

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

		var qs = _.groupBy(indicators, function (definition, key) {
			return [
					definition.duration,
					definition.startOf,
					definition.region
				].join('-');
		});

		return _.map(qs, function (arr) {
			return _.merge.apply(null, arr.concat(function (a, b) {
				if (_.isArray(a)) {
					return a.concat(b);
				}
			}));
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

		this.indicators = {};
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

    var hasMap = _(dashboard.charts)
      .pluck('type')
      .any(t => _.endsWith(t, 'Map'));

    console.log('DashboardActions::hasMap', hasMap);

		this.trigger({
			dashboard  : dashboard,
			region     : region,
			campaign   : campaign,
			loaded     : true,

			regions    : regions,
			campaigns  : _.filter(campaigns, function (c) {
				return c.office_id === region.office_id;
			}),
      dashboards : this.dashboards,
      hasMap     : hasMap
		});
	},

	addChartDefinition : function (chart) {
		var base = _.omit(chart, 'indicators', 'title');

		_.each(chart.indicators, function (id) {
			var duration = moment.duration(chart.timeRange);
			var hash     = [id, chart.startOf, chart.region].join('-');

			if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
				this.indicators[hash] = _.assign({
						duration   : duration,
						indicators : [id]
					}, base);
			}
		}.bind(this));
	}
});

module.exports = DashboardStore;
