'use strict';

var _ = require('lodash');
var d3 = require('d3');

var formats = {
	percent: d3.format('%')
};

var scales = {
	completionClass: function(v) {
		if (v === 0) { return 'statusText-bad'; }
		else if (v === 1) { return 'statusText-good'; }
		else if (v > 0 && v < 1) { return 'statusText-okay'; }
		return null;
	}
};

module.exports = {

	template: require('./template.html'),

	ready: function () {
		
		_.defaults(this.$data, {
			groupSize: 5
		});

		this.$watch('rows', this.updateStats, true, true);

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

		}

	},

	filters: {

		percent: function(v) {
			return formats.percent(v);
		},

		completionClass: function(v) {
			return scales.completionClass(v);
		},

		rowComplete: function() {
			return (this.stats.byRow[this.$index] !== undefined) ? this.stats.byRow[this.$index].complete : null;
		},

		rowTotal: function() {
			return (this.stats.byRow[this.$index] !== undefined) ? this.stats.byRow[this.$index].total : null;
		},

		rowCompletionClass: function() {
			if (this.stats.byRow[this.$index] !== undefined) {
				return scales.completionClass(this.stats.byRow[this.$index].complete / this.stats.byRow[this.$index].total);
			}
			return null;
		}


	},

	components: {
		'uf-cell': require('./cell')
	}
};
