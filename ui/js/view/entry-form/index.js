'use strict';

var _        = require('lodash');
var d3       = require('d3');

var api      = require('../../data/api');
var Dropdown = require('../../component/dropdown');

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			loaded: false,
			regions: [],
			indicators: [],
			indicatorSet: [
				{ 'id': 5 },
				{ 'id': 51 },
				{ 'id': 69 }, 
				{ 'id': 70 }, 
				{ 'id': 160 }, 
				{ 'id': 161 }, 
				{ 'id': 44 }, 
				{ 'id': 43 }, 
				{ 'id': 32 }, 
				{ 'id': 31 }, 
				{ 'id': 158 }, 
				{ 'id': 34 }, 
				{ 'id': 33 }
			],
			pagination: {
				// the_limit: 20,
				// the_offset: 0,
				total_count: 0
			},
			table: {
				loading: false,
				columns: ['region', 'campaign'],
				rows: []
			},
			
			campaigns: [],
			campaign_id: null

		};
	},

	ready: function() {

		this.load();

	},

	attached: function () {
		var self = this;

		this._regions = new Dropdown({
			el     : '#regions',
			source : api.regions,
			mapping: {
				'parent_region_id': 'parent',
				'name'         : 'title',
				'id'           : 'value'
			}
		});
		this._regions.$on('dropdown-value-changed', function (items) {
			self.regions = items;
		});

		// this._indicators = new Dropdown({
		// 	el     : '#indicators',
		// 	source : api.indicators,
		// 	mapping: {
		// 		'short_name': 'title',
		// 		'id'        : 'value'
		// 	}
		// });

		// this._indicators.$on('dropdown-value-changed', function (items) {
		// 	self.indicators = items;
		// });

		this.$on('page-changed', function (data) {
			this.refresh(data);
		});
	},

	computed: {

		hasSelection: function () {
			return this.regions.length > 0;
			// return this.regions.length > 0 && this.indicators.length > 0;
		}

	},

	methods: {

		load: function() {
			var self = this;

			var makeMap = function(data) { 
				if (data.objects) {
					return _.indexBy(data.objects, 'id'); 
				} else {
					return null;
				}
			};

			Promise.all([

					// regions data
					api.regions().then(makeMap),

					// indicators data
					api.indicators().then(makeMap),

					// campaigns data
					api.campaign().then(function(data) {
						if (!data.objects) { return null; }
						return data.objects
							.sort(function(a,b) {
								return a.start_date > b.start_date ? -1 : 1;
							})
							.map(function(d) {
								return {
									text: d.slug,
									value: d.id
								};
							});
					})

				]).done(function(allData) {

					self.$data.regionData = allData[0];
					self.$data.indicators = allData[1];
					self.$data.campaigns = allData[2];

					// set campaign id to first option
					self.$data.campaign_id = self.$data.campaigns[0].value;

					self.$data.loaded = true;

				});

		},

		refresh: function (pagination) {
			// if (!this.hasSelection) {
			// 	return;
			// }

			var self = this;

			// default values for testing
			var regions = [ 12942, 12939, 12929, 12928 ];
			// var regions = [ 12942, 12939, 12929, 12928, 12927, 12926, 12925, 12920, 12913, 12911, 12910 ];

			// get from dropdown
			if (this.hasSelection) {
				regions     = _.map(this.regions, 'value');
			}

			var options = { 
				// campaign_id__in: [ self.$data.campaign_id ],
				campaign_start: '2013-06-01',
				campaign_end: '2013-06-30',
				indicator__in: [],
				region__in: []
			};

			if (pagination) {
				// Prepend "the_" to the pagination options (typically limit and offset)
				// because the datapoint API uses the_limit and the_offset instead of
				// limit and offset like the other paged APIs. See POLIO-194.
				_.forOwn(pagination, function (v, k) {
					options['the_' + k] = v;
				});
			}

			// add regions to request
			if (regions.length > 0) {
				options.region__in = regions;
				// sort region order
				options.region__in = options.region__in.sort(function(a,b) {
					return self.$data.regionData[a].name > self.$data.regionData[b].name ? 1 : -1;
				});
			}

			// add indicators to request
			this.indicatorSet.forEach(function (row) {
				if (row.id) {
					options.indicator__in.push(row.id);
				}
			});

			// define columns
			var columns = [
				{ 
					header: 'Indicator', 
					type: 'label', 
					headerClasses: 'medium-3' 
				}
			];
			// add region names as columns
			options.region__in.forEach(function(region_id) {
				columns.push({
					header: self.$data.regionData[region_id].name,
					type: 'value',
					key: region_id
				});
			});

			// cell formatters
			var numericFormatter = function (v) {
				return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v);
			};

			_.defaults(options, this.pagination);

			this.table.loading = true;

			console.log(options);

			api.datapoints(options).done(function (data) {
				self.table.loading = false;

				self.pagination.the_limit   = Number(data.meta.the_limit);
				self.pagination.the_offset  = Number(data.meta.the_offset);
				self.pagination.total_count = Number(data.meta.total_count);

				// pivot data so that each row contains all region datapoints for one indicator
				// TO DO: this may be broken by pagination (?) and so would need to be grouped differently on the back end
				// TO DO: move this to data transform utility
				var byIndicator = {};
				data.objects.forEach(function (d) {
					d.indicators.forEach(function (ind) {
						if (!byIndicator[ind.indicator]) { byIndicator[ind.indicator] = {}; }
						byIndicator[ind.indicator][d.region] = ind;						
					});
				});

				// assemble data points into rows for table
				var rows = [];
				options.indicator__in.forEach(function(ind) {
					
					var row = [];

					// add columns 
					columns.forEach(function(column) {

						var cell = {
							isEditable: false,
							type: column.type
						};

						switch (column.type) {

							// editable value
							case 'value':
								cell.isEditable = true;
								cell.format = numericFormatter;
								cell.classes = 'numeric';
								cell.value = byIndicator[ind] && byIndicator[ind][column.key] ? byIndicator[ind][column.key].value : null;
								break;

							// indicator name
							case 'label':
								cell.value = self.$data.indicators[ind] ? self.$data.indicators[ind].name : 'Missing Data for Indicator'+ind;
								break;

						}

						// add cell to row
						row.push(cell);
					});

					// add row to main array
					rows.push(row);
				});

				self.table.rows = rows;
				self.table.columns = columns;

			});
		},

		download: function () {
			// if (!this.hasSelection) {
			// 	return;
			// }

			// this.downloading = true;

			// var indicators   = _.map(this.indicators, 'value');
			// var regions      = _.map(this.regions, 'value');
			// var query        = {
			// 	// FIXME: Hack to get around no way of setting no limit for the 12/9 demo.
			// 	'the_limit'  : 10000000,
			// 	'format'     : 'csv',
			// 	'uri_display': 'slug'
			// };

			// if (indicators.length < 1) {
			// 	this.$data.src = '';
			// 	return;
			// }

			// query.indicator__in = indicators;
			// if (regions.length > 0) {
			// 	query.region__in = regions;
			// }

			// this.$set('src', api.datapoints.toString(query));
		},

		previous: function () {
			if (this.pagination.the_offset < 1) {
				return;
			}

			this.pagination.the_offset = Math.max(0, this.pagination.the_offset - this.pagination.the_limit);
			this.refresh();
		},

		next: function () {
			this.pagination.the_offset += this.pagination.the_limit;
			this.refresh();
		}
	}
};
