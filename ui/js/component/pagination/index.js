'use strict';

module.exports = {
	template: require('./template.html'),
	data: function () {
		return {
			limit: 0,
			offset: 0,
			total_count: 0
		};
	},
	methods: {
		setPage: function (page) {
			if (page < 1 || page > this.pageCount || page === this.current) {
				return;
			}

			console.log('set page: ' + page);
			this.$dispatch('page-changed', {
				limit: this.limit,
				offset: this.limit * (page - 1)
			});
		},
		first: function () {
			this.setPage(1);
		},
		previousPage: function () {
			this.setPage(this.current - 1);
		},
		nextPage: function () {
			this.setPage(this.current + 1);
		},
		last: function () {
			this.setPage(this.pageCount);
		}
	},
	computed: {
		firstPage: function () {
			return this.offset === 0;
		},
		lastPage: function () {
			return (this.total_count - this.offset) <= this.limit;
		},
		pageCount: function () {
			return this.limit < 1 ? 0 : Math.ceil(this.total_count / this.limit);
		},
		current: function () {
			return this.offset / this.limit + 1;
		},
		jumpBack: function () {
			var lower = this.current - 2;
			if (lower < 3) {
				return false;
			}

			return Math.ceil(lower / 2);
		},
		jumpForward: function () {
			var upper = this.current + 2,
				total = this.pageCount;

			if (upper > (total - 2)) {
				return false;
			}

			return upper + Math.floor((total - upper) / 2);
		},
		pages: function () {
			var total = this.pageCount,
				current = this.current,
				lower = Math.max(1, current - 2),
				upper = Math.min(total, lower + 4),
				pages = [];

			for (var i = lower; i <= upper; ++i) {
				pages.push({
					number: i,
					current: i === current
				});
			}

			return pages;
		}
	}
};
