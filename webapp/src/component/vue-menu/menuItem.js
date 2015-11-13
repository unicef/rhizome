'use strict'

import _ from 'lodash'

export default {
  replace: true,
  inherit: true,
  template: require('./menuItem.html'),

  data: function () {
    return {
      title: '',
      children: [],
      open: false,
      depth: 0
    }
  },

  computed: {
    hasChildren: function () {
      return !this.filtered && _.isArray(this.children) && this.children.length > 0
    },

    showChildren: function () {
      return this.hasChildren && this.open
    },

    style: function () {
      // FIXME: It's unfortunate to hard-code the padding amounts. It would be
      // way cooler to interrogate the CSS for the object to determine
      // these values, or use

      if (this.filter) {
        return {
          'padding-left': '5px'
        }
      }

      return {
        'padding-left': (5 + (17 * this.depth)) + 'px'
      }
    }
  },

  methods: {
    onClick: function (event, data) {
      event.preventDefault()
      this.$dispatch(this.changeEvent, data)
      this.open = false
    },

    toggleChildren: function (evt) {
      evt.stopPropagation()

      this.open = !this.open
    }
  }

}
