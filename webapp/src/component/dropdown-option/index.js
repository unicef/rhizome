'use strict'
export default {
  template: require('./template.html'),
  computed: {
    display: function () {
      return this.$data.title || this.$data.value
    }
  },
  methods: {
    onClick: function () {
      this.$dispatch('optionClick', this)
    }
  }
}
