'use strict';

var _ = require('lodash');
var d3 = require('d3');

var formats = {
	percent: d3.format('%')
};

module.exports = {
	template: require('./template.html'),

	ready: function () {
		
		_.defaults(this.$data, {
			groupSize: 5
		});

		this.$watch('rows', function() {
			this.updateStats();
		}, true);

	},

	methods: {

		// update table stats
		updateStats: function() {
			var self = this;

			var newCounter = function() {
				return {
					'complete': 0,
					'total': 0
				};
			};

			var stats = {
				total: newCounter(),
				byRow: [],
				byColumn: []
			};

			if (self.rows.length > 0) {

				_.forEach(self.rows, function(row, rowIndex) {

					if (stats.byRow[rowIndex] === undefined) {
						stats.byRow[rowIndex] = newCounter();
					}

					_.forEach(row, function(cell, colIndex) {

						if (stats.byColumn[colIndex] === undefined) {
							stats.byColumn[colIndex] = newCounter();
						}

						if (cell.isEditable) {

							stats.total.total ++;
							stats.byRow[rowIndex].total ++;
							stats.byColumn[colIndex].total ++;

							if (!_.isNull(cell.value)) {
								stats.total.complete ++;
								stats.byRow[rowIndex].complete ++;
								stats.byColumn[colIndex].complete ++;
							}

						}

					}); // end column loop

				}); // end row loop

			}

			self.$set('stats', stats);

		},

		summarize: function(i, type) {
			var stats = this.$get('stats');
			if (!stats) { return null; }

			var statSet;
			if (type === 'column') {
				statSet = stats.byColumn;
			} else if (type === 'row') {
				statSet = stats.byRow;
			}

			if (statSet && i < statSet.length) {
				var v = statSet[i];
				return v.complete + ' / ' + v.total;
			} else {
				return null;
			}

		}		

	},

	filters: {

		// proxy to method
		summarize: function(i, type) {
			return this.$parent.summarize(i, type);
		},

		percent: function(v) {
			return formats.percent(v);
		}

	},

	components: {
		'uf-cell': require('./cell')
	}
};
