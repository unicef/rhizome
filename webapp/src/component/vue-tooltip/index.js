/* global window */
'use strict'

var _ = require('lodash')
var Vue = require('vue')

var dom = require('../../util/dom')

module.exports = {
    template: require('./template.html'),

    inherit: true,
    replace: true,

    paramAttributes: [
        'data-orientation'
    ],

    data: function () {
        return {
            orientation: 'top',
            show: false,
            delay: 500,
            template: 'tooltip-default',

            top: 0,
            right: 0,
            bottom: 0,
            left: 0
        }
    },

    ready: function () {
        this.$root.$on('tooltip-show', this.showTooltip)
        this.$root.$on('tooltip-hide', this.hideTooltip)
    },

    methods: {
        reposition: function () {
            var offset
            var doc

            if (this._position) {
                offset = {
                    top: this._position.y,
                    right: this._position.x,
                    bottom: this._position.y,
                    left: this._position.x
                }

                doc = window.document.body
            } else if (this._parentEl) {
                offset = dom.documentOffset(this._parentEl)
                doc = this._parentEl.ownerDocument.documentElement
            } else {
                return
            }

            switch (this.orientation) {
            case 'right':
                this.top = offset.top + 'px'
                this.right = 'auto'
                this.bottom = 'auto'
                this.left = offset.right + 'px'
                break

            case 'bottom':
                this.top = offset.bottom + 'px'
                this.right = 'auto'
                this.bottom = 'auto'
                this.left = offset.left + 'px'
                break

            case 'left':
                this.top = offset.top + 'px'
                this.right = (doc.clientWidth - offset.left) + 'px'
                this.bottom = 'auto'
                this.left = 'auto'
                break

            default:
                this.top = 'auto'
                this.right = 'auto'
                this.bottom = (doc.clientHeight - offset.top) + 'px'
                this.left = offset.left + 'px'
                break
            }

            Vue.nextTick(this.reorient)
        },

        reorient: function () {
            var el = this.$el
            var offset = dom.viewportOffset(el)
            var reposition = false

            if (this.orientation !== 'bottom' && offset.top < 0) {
              this.orientation = 'bottom'
              reposition = true
            }

            if (reposition) {
                this.reposition()
            }
        },

        hideTooltip: function (options) {
            if (this._parentEl === options.el) {
                this.show = false
                this._parentEl = null
                this._position = null

                // Preempt showing the tooltip
                if (this._timer) {
                    window.clearTimeout(this._timer)
                }

                window.removeEventListener('resize', this.reposition)
            }
        },

        showTooltip: function (options) {
            // Update the position, if we have one, no matter what, this way the
            // tooltip will show up at the right place, even if we haven't
            // displayed it yet.
            this._position = options.position

            // True if we've already started a timer for this tooltip
            var timerStarted = this._timer && this._parentEl === options.el

            // Don't reset the timer if one's already started
            if (timerStarted) {
                return
            }

            this._parentEl = options.el

            var self = this

            // Set the delay to 0 if we have already shown the tooltip
            var delay = self.show ? 0 : self.delay

            // Wait for the delay
            self._timer = setTimeout(function () {
                // FIXME: Merging in the options doesn't account for the fact that if
                // no template is passed, it keeps the previously used template, instead
                // of reverting to the default template.
                // Crude version of Vue's mergeOptions...
                _.forOwn(options.data, function (v, k) {
                    self.$set(k, v)
                })

                self.reposition()
                window.addEventListener('resize', self.reposition)

                self.show = true
                self._timer = null
            }, delay)
        }
    },

    partials: {
        'tooltip-default': '{{ text }}'
    }

}
