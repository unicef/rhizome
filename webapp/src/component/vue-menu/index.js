/* global window */

'use strict'

var _ = require('lodash')
var Vue = require('vue')

var dom = require('util/dom')

function findMatches (item, re) {
  var matches = []

  if (re.test(item.title)) {
    matches.push(item)
  }

  if (item.children) {
    item.children.forEach(function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

module.exports = {
  replace: true,
  template: require('./template.html'),

  paramAttributes: [
    'data-change-event',
    'data-searchable',
    'full-size-menu' // used to remove the fa-stack class on the menu-button element, so the menu can be expanded into a full size button
  ],

  data: function () {
    return {
      items: [],
      open: false,
      pattern: '',
      searchable: false,

      marginLeft: 0,
      maxHeight: 'none',
      orientation: 'center',

      changeEvent: 'menu-item-click'
    }
  },

  ready: function () {
    window.addEventListener('resize', this.onResize)
    window.addEventListener('scroll', this.onResize)
  },

  computed: {
    filtered: function () {
      return this.pattern.length > 2
    },

    filteredItems: function () {
      if (!this.filtered) {
        return this.items
      }

      var items = []
      var pattern = this.pattern

      _.forEach(this.items, function (item) {
        items = items.concat(findMatches(item, new RegExp(pattern, 'gi')))
      })

      return items
    }
  },

  methods: {
    toggleMenu: function (event) {
      event.stopPropagation()

      this.open = !this.open
      window.addEventListener('click', this.onClick)

      Vue.nextTick(this.onResize)
    },

    clearSearch: function (evt) {
      evt.stopPropagation()
      this.pattern = ''
    },

    onClick: function () {
      this.open = false
      this.pattern = ''
    },

    onResize: function () {
      if (!this.open) {
        return
      }

      var el = dom.dimensions(this.$el)
      var menu = dom.dimensions(this.$$.menu)
      var items = dom.dimensions(this.$$.itemList)
      var offset = dom.viewportOffset(this.$el)

      this.maxHeight = window.innerHeight - offset.top - (menu.height - items.height)

      var rightEdge = offset.left + (el.width / 2) + (menu.width / 2)
      var leftEdge = offset.left + (el.width / 2) - (menu.width / 2)

      if (menu.width > window.innerWidth) {
        this.orientation = 'left'
        this.marginLeft = 0
      } else if (el.width >= menu.width) {
        this.orientation = 'center'
        this.marginLeft = -menu.width / 2
      } else if (leftEdge < 0) {
        this.orientation = 'left'
        this.marginLeft = 0
      } else if (rightEdge > window.innerWidth) {
        this.orientation = 'right'
        this.marginLeft = 0
      } else {
        this.orientation = 'center'
        this.marginLeft = -menu.width / 2
      }
    }
  },

  components: {
    'vue-menuitem': require('./menuItem.js')
  }
}
