/* global window */

'use strict'

import _ from 'lodash'
import Vue from 'vue'

import dom from '../../util/dom'
import util from '../../util/data'
import treeify from '../../data/transform/treeify'

export default Vue.extend({
  template: require('./template.html'),

  // Object mapping property names of response objects to property names for the
  // VM. Useful for setting the 'title, ' 'value, ' and 'parent' properties of the
  // dropdown items.
  mapping: {},

  // (Optional) Function for fetching data.
  source: null,

  paramAttributes: [
    'loading',
    'multi',
    'placeholder',
    'searchable',
    'data-sort-dsc',
    'data-sort-by'
  ],

  data: function () {
    return {
      itemTree: [],
      items: [],
      loading: false,
      menuHeight: 0,
      menuX: 0,
      open: false,
      opening: false,
      pattern: '',
      selection: {},
      sortBy: 'title',
      sortDsc: false
    }
  },

  ready: function () {
    this.multi = util.parseBool(this.multi)
    this.searchable = util.parseBool(this.searchable)
    this.sortDsc = util.parseBool(this.sortDsc)

    this.load()
  },

  computed: {
    isFiltered: function () {
      return this.pattern.length > 2
    },

    filtered: function () {
      var pattern = new RegExp(this.pattern, 'gi')

      return this.items.filter(function (d) {
        return pattern.test(d.title)
      })
    },

    hasSelection: function () {
      return _.keys(this.selection).length > 0
    },

    title: function () {
      if (!this.hasSelection) {
        return this.placeholder
      }

      return _(this.selection)
        .values()
        .pluck('title')
        .value()
        .join(', ')
    }
  },

  methods: {
    toggle: function () {
      this.opening = this.open = !this.open

      if (this.searchable) {
        var inpt = this.$el.getElementsByTagName('input')[0]

        // Reset the query
        this.pattern = ''

        if (this.open) {
          inpt.focus()
        }
      }

      if (this.open) {
        window.addEventListener('resize', this)
        window.addEventListener('click', this)
        window.addEventListener('keyup', this)
        this.invalidateSize()

        this.$el.getElementsByTagName('ul')[0].scrollTop = 0
      } else {
        window.removeEventListener('resize', this)
        window.removeEventListener('click', this)
        window.removeEventListener('keyup', this)
      }
    },

    toggleItem: function (item) {
      var self = this
      if (!this.multi) {
        if (this.selection) {
          var keys = _.keys(self.selection)
          _.each(keys, function (key) {
            delete self.selection[key]
          })
        }
        this.selection[item.value] = item
        this.open = false
        this.selection.__ob__.notify()
      } else {
        if (this.selection.hasOwnProperty(item.value)) {
          delete this.selection[item.value]
        } else {
          this.selection[item.value] = item
        }

        this.selection.__ob__.notify()
      }

      this.$emit('dropdown-value-changed', this.selection)
    },

    handleEvent: function (evt) {
      switch (evt.type) {
        case 'keyup':
          // ESC
          if (evt.keyCode === 27) {
            this.open = false
          }
          break

        case 'click':
          if (this.opening) {
            this.opening = false
          } else if (!dom.contains(this.$el.getElementsByClassName('container')[0], evt)) {
            this.open = false
          }
          break

        case 'resize':
          this.invalidateSize()
          break

        default:
          break
      }
    },

    invalidateSize: _.throttle(function () {
      var menu = this.$el.getElementsByClassName('container')[0]
      var ul = menu.getElementsByTagName('ul')[0]
      var style = window.getComputedStyle(menu)
      var marginBottom = parseInt(style.getPropertyValue('margin-bottom'), 10)
      var marginRight = parseInt(style.getPropertyValue('margin-right'), 10)
      var offset = dom.viewportOffset(ul)
      var dims

      if (this.multi) {
        dims = dom.dimensions(menu.getElementsByClassName('selection-controls')[0], true)
        marginBottom += dims.height
      }

      dims = dom.dimensions(menu)

      this.menuHeight = window.innerHeight - offset.top - marginBottom
      this.menuX = Math.min(0, window.innerWidth - dom.viewportOffset(this.$el).left - dims.width - marginRight)
    }, 100, { leading: false }),

    select: function (value) {
      if (!value) {
        return
      }

      // Collect the current selection outside of the VM to prevent too many
      // updates to the UI
      var selection = {}
      this.forAll(function (item) {
        if (item.value === value) {
          selection[item.value] = item
        }
      })

      // Trigger an update of the VM
      this.selection = selection
    },

    clear: function () {
      this.selection = {}
      this.$emit('dropdown-value-changed', this.selection)
    },

    invert: function () {
      var selection = {}

      this.forAll(function (item) {
        if (!this.selection.hasOwnProperty(item.value)) {
          selection[item.value] = item
        }
      })

      this.selection = selection
      this.$emit('dropdown-value-changed', this.selection)
    },

    selectAll: function () {
      var selection = {}

      this.forAll(function (item) {
        selection[item.value] = item
      })

      this.selection = selection
      this.$emit('dropdown-value-changed', this.selection)
    },

    load: function (params, accumulator) {
      if (!this.$options.source) {
        return
      }

      params = params || {}
      accumulator = accumulator || []

      var self = this
      var source = self.$options.source
      var mapping = self.$options.mapping

      self.loading = true

      source(params)
        .then(function (data) {
          return {
            meta: data.meta,
            errors: data.errors,
            objects: _.map(data.objects, function (v) {
              return _.defaults(util.rename(v, mapping), { selected: false })
            })
          }
        })
        .then(function (data) {
          var meta = data.meta

          accumulator = accumulator.concat(data.objects)

          if (meta.limit && meta.limit !== 0 && meta.limit + meta.offset < meta.total_count) {
            self.load({
              limit: meta.limit,
              offset: meta.offset + meta.limit
            }, accumulator)
          } else {
            self.itemTree = treeify(accumulator, 'value')
            self.items = accumulator
            self.loading = false

            self.select(self.$options.defaults)
            self.$emit('dropdown-value-changed', self.selection)
          }
        })
    },

    /**
     * Apply a callback to each item in the dropdown.
     *
     * Traverses the item tree and runs `cb` on each item. The context for the
     * `cb` will always be the component.
     *
     * @param {function} cb The callback executed on each item
     */
    forAll: function (cb) {
      // Work queue needs to be copied from items so that we don't shift items
      // off of the data model we use for display
      var q = [].concat(this.items)

      while (q.length > 0) {
        var item = q.shift()

        cb.call(this, item)

        q.push.apply(q, item.children)
      }
    }
  },

  filters: {
    isSelected: function (value) {
      return this.selection.hasOwnProperty(value)
    }
  },

  events: {
    'dropdown-item-toggle': 'toggleItem'
  },

  components: {
    'dropdown-item': require('./item')
  }

})
