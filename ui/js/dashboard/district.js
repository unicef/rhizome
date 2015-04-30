/* global window */
'use strict';

var _      = require('lodash');
var moment = require('moment');

var api             = require('data/api');
var format          = require('util/format');
var indexIndicators = require('data/transform/indexIndicators');
var variables       = require('data/transform/variables');
var util            = require('util/data');

function normalize(d) {
	var total = _(d.indicators).values().sum();

	if (total === 0) {
		return d;
	}

	_.each(d.indicators, function (v, k) {
		d.indicators[k] /= total;
	});

	return d;
}

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

			dateFormat : format.timeAxis,
			pctFormat  : d3.format('.1%'),

			loading           : true,
			immunityGap       : new Array(3),
			immunityGapDomain : null,
			immunityGapRange  : [0, 1]
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

			this.loading = false;

			var startDate       = util.accessor('campaign.start_date');
			var sort            = _.partialRight(_.sortBy, 'x');
			var defined         = _.partialRight(util.defined, util.accessor('y'), _, _);
			var datumTransform  = _.curryRight(createDataPoint);
			var seriesTransform = _.curryRight(createDataSeries);

			var series = _(data)
				.map(indexIndicators)
				.map(normalize)
				.groupBy('region')
				.map(sort)
				.value();

			this.immunityGapRange = [0, _(series)
				.flatten()
				.pluck('indicators')
				.map(_.values)
				.flatten()
				.max()];

			this.immunityGap.$set(0, _(series)
				.map(seriesTransform(431, _, _))
				.reject(_.isEmpty)
				.value());

			this.immunityGap.$set(1, _(series)
				.map(seriesTransform(432, _, _))
				.reject(_.isEmpty)
				.value());

			this.immunityGap.$set(2, _(series)
				.map(seriesTransform(433, _, _))
				.reject(_.isEmpty)
				.value());
		},

		error : function () {
			window.alert('Dammit!');
		},

		load : function () {
			this.loading = true;

			if (!(this.campaign && this.region)) {
				return;
			}

			var q = {
				parent_region__in : this.region.id,
				level             : 'district'
			};

			var start = moment(this.campaign.start_date)
				.subtract(1, 'year');

			var end = moment(this.campaign.start_date);

			this.immunityGapDomain = [
				start.toDate().getTime(),
				end.toDate().getTime()
			];

			// Create a function that plucks the 'objects' property off of the API
			// response objects and concatenates them
			var concatenateData = function (data) {
				return _(data).pluck('objects').flatten().value();
			};

			var districts = api.datapoints({
				parent_region__in : this.region.id,
				level             : 'district',
				indicator__in     : [431,432,433],
				campaign_start    : start.format('YYYY-MM-DD'),
				campaign_end      : end.format('YYYY-MM-DD')
			});

			var national = api.datapoints({
				region__in     : this.region.id,
				indicator__in  : [431,432,433],
				campaign_start : start.format('YYYY-MM-DD'),
				campaign_end   : end.format('YYYY-MM-DD')
			});

			Promise.all([districts, national])
				.then(function (data) {
					return concatenateData(data);
				}, this.error)
				.then(this.dataReceived, this.error);
		}
	},

	watch : {
		campaign : 'load',
		region   : 'load'
	}
};
