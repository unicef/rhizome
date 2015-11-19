import _ from 'lodash'

export default {
  replace: true,
  template: require('./item.html'),

  data: function () {
    return {
      padding: 17,
      level: 0,
      open: false,
      selected: false,
      children: [],
      selection: {}
    }
  },

  computed: {
    selected: function () {
      return this.selection.hasOwnProperty(this.value)
    },

    hasChildren: function () {
      return this.children && this.children.length > 0
    },

    indent: function () {
      return (this.padding * this.level) + 'px'
    }
  },

  methods: {
    onClick: function () {
      this.$dispatch('dropdown-item-toggle', _.assign({}, this.$data))
    },

    toggleFolder: function (e) {
      this.open = !this.open

      // Prevent opening a folder from toggling that item
      e.stopPropagation()
    }
  }

}
