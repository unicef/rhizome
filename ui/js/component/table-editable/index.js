'use strict';

var _ = require('lodash');

module.exports = {
	template: require('./template.html'),

	ready: function () {
		_.defaults(this.$data, {
			groupSize: 5
		});
	},

	methods: {

		// summarize completion
		summarize: function(k, type) {

			// assemble editable cells according to which type of summarization we're doing
			var editableCells; 
			if (type === 'byRow') {
				editableCells = k.filter(function(d) { return d.isEditable; });
			}
			else if (type === 'byColumn') {
				// return null immediately if this is not a "value" column
				if (this.columns[k].type !== 'value') {
					return '';
				}
				editableCells = _(this.rows)
									.map(function(row) { return row[k]; })
									.filter(function(d) { return (d) ? d.isEditable : false; })
									.value();
			} else {
				// editableCells = this.$data.rows.filter(function(d,i) { return i==k && d.isEditable; });
			}

			var valueCount = _.reduce(editableCells, function(count, cell) { 
					if (!_.isNull(cell.value)) { count ++; }
					return count;
				}, 0);
			var total = editableCells.length;
			var summary = valueCount + ' / ' + total;

			return summary;
		}		

	},

	filters: {

		// summarize proxy as filter
		summarize: function(k, type) {
			return this.summarize(k, type);
		}

	},

	components: {
		'uf-cell': require('./cell')
	}
};
