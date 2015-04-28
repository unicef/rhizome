/* global window */
'use strict';

var _      = require('lodash');
var moment = require('moment');

var api             = require('data/api');
var indexIndicators = require('data/transform/indexIndicators');
var variables       = require('data/transform/variables');
var util            = require('util/data');

module.exports = {
	template : require('./district.html'),

	data : function () {
		return {
			annotation     : null,
			campaign       : null,
			currentSection : null,
			highlights     : [],
			region         : null,
			sections       : [],

			immunityGap    : new Array(3)
		};
	},

	methods : {
		dataReceived : function (data) {
			function createDataPoint(d, indicator) {
				return _.assign(_.pick(d, 'campaign', 'region'), {
					indicator : indicator,
					x         : startDate(d),
					y         : d.indicators[indicator]
				});
			}

			function createDataSeries(arr, indicator) {
				return _(arr)
					.map(datumTransform(indicator, _, _))
					.filter(defined)
					.value();
			}

			var startDate       = util.accessor('campaign.start_date');
			var sort            = _.curryRight(_.sortBy)('x');
			var defined         = _.curryRight(util.defined)(util.accessor('y'), _, _);
			var datumTransform  = _.curryRight(createDataPoint);
			var seriesTransform = _.curryRight(createDataSeries);

			var series = _(data.objects)
				.map(indexIndicators)
				.groupBy('region')
				.map(sort)
				.value();

			this.immunityGap[0] = _(series)
				.map(seriesTransform(431, _, _))
				.reject(_.isEmpty)
				.value();

			this.immunityGap[1] = _(series)
				.map(seriesTransform(432, _, _))
				.reject(_.isEmpty)
				.value();

			this.immunityGap[2] = _(series)
				.map(seriesTransform(433, _, _))
				.reject(_.isEmpty)
				.value()
		},

		error : function () {
			window.alert('Dammit!');
		},

		load : function () {
			if (!(this.campaign && this.region)) {
				return;
			}

			var q = {
				parent_region__in : this.region.id,
				level             : 'district'
			};

			var start = moment(this.campaign.start_date)
				.subtract(1, 'year')
				.format('YYYY-MM-DD');

			var end = moment(this.campaign.start_date).format('YYYY-MM-DD');

			api.datapoints(_.assign({
					indicator__in  : [431,432,433],
					campaign_start : start,
					campaign_end   : end
				}, q))
				.then(this.dataReceived, this.error);
		}
	},

	watch : {
		campaign : 'load',
		region   : 'load'
	}
};
