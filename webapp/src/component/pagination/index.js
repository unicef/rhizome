'use strict'

module.exports = {
    template: require('./template.html'),

    data: function () {
        return {
            limit: 0,
            offset: 0,
            total_count: 0,
            window_size: 1
        }
    },

    computed: {
        hasPrevious: function () {
            return this.offset > 0
        },

        hasNext: function () {
            return (this.offset + this.limit) < this.total_count
        },

        pageCount: function () {
            return this.limit < 1 ? 0 : Math.ceil(this.total_count / this.limit)
        },

        current: function () {
            return (this.offset / this.limit) + 1
        },

        pages: function () {
            var pages = []
            // If the total number of pages is small enough that we can fit the entire
            // thing in the same number of links it would take with jumps, just render
            // all the numbers. This avoids pagination controls that do the following:
            // 1...3 4, where the jump (...) just takes you to page 2.
            if (this.pageCount <= (this.window_size * 2) + 5) {
                for (var i = 1; i <= this.pageCount; i++) {
                    pages.push({ number: i })
                }

                return pages
            }

            // Start with page 2 because page 1 is always shown.
            var page = Math.max(2, this.current - this.window_size)
            pages[0] = { number: 1 }

            if (page > 2) {
                pages.push({
                    number: Math.ceil(page / 2),
                    jump: true
                })
            }

            for (var l = Math.min(this.pageCount - 1, this.current + this.window_size); page <= l; page++) {
                pages.push({ number: page })
            }

            if (page < this.pageCount) {
                pages.push({
                    number: Math.floor(page + (this.pageCount - page) / 2),
                    jump: true
                })
            }

            pages.push({ number: this.pageCount })

            return pages
        }
    },

    methods: {
        setPage: function (page) {
            if (page < 1 || page > this.pageCount || page === this.current) {
                return
            }

            this.$dispatch('page-changed', {
                limit: this.limit,
                offset: this.limit * (page - 1)
            })
        }
    }

}
