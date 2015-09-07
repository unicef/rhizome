'use strict';

var _      = require('lodash');
var Reflux = require('reflux');
var moment = require('moment');

var api      = require('data/api');
var builtins = require('dashboard/builtin');

var DashboardStore = Reflux.createStore({

	listenables : [require('actions/DashboardActions')],

	init : function () {

		this.loaded = false;
		this.indicators = {};

		Promise.all([api.regions({parent_region_id: 1}), api.campaign()])
			.then(function (responses) {
        var regionIdx = _.indexBy(responses[0].objects, 'id');

				this.regions    = responses[0].objects;
				this.campaigns  = responses[1].objects;

        _.each(this.regions, function (r) {
          r.region_type = regionIdx[r.region_type_id];
          r.parent = regionIdx[r.parent_region_id];
        });

				this.loaded = true;

        this.trigger({
          loaded    : this.loaded,
          regions   : this.regions,
          campaigns : this.campaign
        });
			}.bind(this));
	},

	getQueries : function () {
		var indicators = this.indicators;
		var qs = _.groupBy(indicators, function (definition, key) {
			return [
					definition.duration,
					definition.startOf,
					definition.regions
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
		var dashboard  = this.dashboard = definition.dashboard;
		var region  	 = dashboard.regions[0];
		// var region = _.find(regions, function (r) {
		// 		return r.id === this.region_id;
		// 	}.bind(this));

		this.date      = definition.date || this.date;

		if (!this.loaded) {
			return;
		}

		this.indicators = {};
		_.each(dashboard.charts, this.addChartDefinition);

		var campaigns = this.campaigns;
		var regions   = this.regions;

		var regionIdx       = _.indexBy(regions, 'id');
		var topLevelRegions = _(regions)
			.filter(function (r) {
				return !regionIdx.hasOwnProperty(r.parent_region_id);
			})
			.sortBy('name');

		var campaign = _(campaigns)
				.filter(function (c) {
					return c.office_id === 1 && //FIXME
					(!this.date || _.startsWith(c.start_date, this.date));
				}.bind(this))
				.sortBy('start_date')
				.last();

    var hasMap = _(dashboard.charts)
      .pluck('type')
      .any(t => _.endsWith(t, 'Map'));

		this.trigger({
			dashboard  : this.dashboard,
			region     : region,
			campaign   : campaign,
			loaded     : true,

			regions    : regions,
			campaigns  : _.filter(campaigns, function (c) {
				return c.office_id === 1 ; //FIXME
			}),
      hasMap     : hasMap,
		});
	},

  onSetRegion : function (id) {
    var region = _.find(this.regions, function (r) {
        return r.id === id;
      }.bind(this));

    if (region) {
      this.trigger({
        region : region
      });
    }
  },

	addChartDefinition : function (chart) {
		var base = _.omit(chart, 'indicators', 'title');

		_.each(chart.indicators, function (id) {
			var duration = !_.isNull(_.get(chart, 'timeRange', null)) ? moment.duration(chart.timeRange) : Infinity;
			var hash     = [id, chart.startOf, chart.regions].join('-');

			if (!this.indicators.hasOwnProperty(hash) || duration > this.indicators[hash].duration) {
				this.indicators[hash] = _.defaults({
						duration   : duration,
						indicators : [id]
					}, base);
			}
		}.bind(this));
	}
});

module.exports = DashboardStore;
