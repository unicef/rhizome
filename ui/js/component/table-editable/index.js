'use strict';

var _ = require('lodash');
var d3 = require('d3');

var formats = {
	percent: d3.format('%')
};

var scales = {
	completionColor: function(v) {
		if (v === 0) { return '#EC1C24'; }
		else if (v === 1) { return '#29A13A'; }
		else if (v > 0 && v < 1) { return 'rgb(242, 129, 0)'; }

		// if (v === 0) { return '#FC5959'; }
		// else if (v === 1) { return '#91cf60'; }
		// else if (v > 0 && v < 0.34) { return '#fc8d59'; }
		// else if (v >= 0.34 && v < 0.67) { return '#fee08b'; }
		// else if (v >= 0.67 && v < 1) { return '#d9ef8b'; }

		else { return 'inherit'; }
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

			console.log(stats);
			self.$set('stats', stats);

		}

	},

	filters: {

		percent: function(v) {
			return formats.percent(v);
		},

		completionColor: function(v) {
			return scales.completionColor(v);
		},

		rowComplete: function() {
			return (this.stats.byRow[this.$index] !== undefined) ? this.stats.byRow[this.$index].complete : null;
		},

		rowTotal: function() {
			return (this.stats.byRow[this.$index] !== undefined) ? this.stats.byRow[this.$index].total : null;
		},

		rowCompletionColor: function() {
			console.log(this);
		}


	},

	components: {
		'uf-cell': require('./cell')
	}
};
