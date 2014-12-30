'use strict';

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			limit      : 0,
			offset     : 0,
			total_count: 0,
			window_size: 1,
		};
	},

	computed: {
		hasPrevious: function () {
			return this.offset > 0;
		},

		hasNext: function () {
			return (this.offset + this.limit) < this.total_count;
		},

		pageCount: function () {
			return this.limit < 1 ? 0 : Math.ceil(this.total_count / this.limit);
		},

		current: {
			get: function () {
				return this.offset / this.limit + 1;
			},

			set: function (page) {
				if (page < 1 || page > this.pageCount || page === this.current) {
					return;
				}

				this.$dispatch('page-changed', {
					limit: this.limit,
					offset: this.limit * (page - 1)
				});
			}
		},

		pages: function () {
			// Start with page 2 because page 1 is always shown.
			var page  = Math.max(2, this.current - this.window_size);
			var pages = [{ number: 1 }];

			if (page > 2) {
				pages.push({
					number: Math.floor((page - 1) / 2),
					jump  : true
				});
			}

			while (page <= Math.min(this.pageCount - 1, this.current + this.window_size)) {
				pages.push({ number: page });
				page++;
			}

			if (page < this.pageCount - 1) {
				pages.push({
					number: Math.ceil(page + (this.pageCount - page) / 2),
					jump  : true
				});
			}

			pages.push({ number: this.pageCount });

			return pages;
		}

	}

};
