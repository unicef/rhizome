'use strict'
var Vue = require('vue')
var _ = require('lodash')
var api = require('../../data/api')
var treeify = require('../../data/transform/treeify')
var ancestoryString = require('../../data/transform/ancestryString')
var MenuVue = require('../../component/vue-menu')

module.exports = {
  template: require('./template.html'),
  data: function () {
    return {
      locations: [],
      groups: []
    }
  },
  created: function () {
    var self = this
    self.$set('locationalAccessLoading', true)
    var MenuComponent = Vue.extend(MenuVue)

    api.groups().then(function (response) {
      var groups = response.objects
      api.user_groups({'user': self.$parent.$data.user_id}).then(function (data) {
        _.forEach(groups, function (group) {
          group.active = _.some(data.objects, {'group_id': group.id})
        })
        self.$set('groups', response.objects)
      })
    })

    api.locations().then(function (items) {
      self.loadlocationalAccess()
      self.location_map = _.indexBy(items.objects, 'id')
      var locations = _(items.objects)
        .map(function (location) {
          return {
            'title': location.name,
            'value': location.id,
            'id': location.id,
            'parent': location.parent_location_id
          }
        })
        .sortBy('title')
        .reverse() // I do not know why this works, but it does
        .thru(_.curryRight(treeify)('id'))
        .thru(ancestoryString)
        .value()
      self.$set('locations', locations)
    }).then(function () {
      self.locationMenu = new MenuComponent({
        el: '#locations'
      })
      self.locationMenu.items = self.$data.locations
      self.locationMenu.$on('field-selected', self.addlocationalAccess)
    })
  },
  methods: {
    addRemoveUserGroup: function (e) {
      var groupId = e.target.getAttribute('data-group-id')
      if (e.target.checked) {
        api.map_user_group({'user_id': this.$parent.$data.user_id, 'group_id': groupId})
      } else {
        api.map_user_group({'user_id': this.$parent.$data.user_id, 'group_id': groupId, id: ''})
      }
    },
    addlocationalAccess: function (data) {
      var self = this
      self.$set('locationalAccessLoading', true)
      api.set_location_permission({ user_id: this.$parent.$data.user_id, location_id: data, read_write: 'r' }).then(function () {
        self.loadlocationalAccess()
      })
    },
    deletelocationalAccess: function (data) {
      var self = this
      var readWrite = _.find(self.$get('location_permissions'), { location_id: data }).read_write
      api.set_location_permission({ user_id: this.$parent.$data.user_id, location_id: data, read_write: readWrite, id: '' }).then(function () {
        self.loadlocationalAccess()
      })
    },
    updatelocationalAccessCanRead: function (e) {
      var locationId = e.target.getAttribute('data-location-id')
      var internalId = e.target.getAttribute('data-internal-id')
      var readWrite = (e.target.checked ? 'w' : 'r')
      api.set_location_permission({ user_id: this.$parent.$data.user_id, location_id: locationId, read_write: readWrite, id: internalId })
    },

    loadlocationalAccess: function () {
      var self = this

      api.location_permission({ user: this.$parent.$data.user_id }).then(function (data) {
        var locations = data.objects
        _.forEach(locations, function (location) {
          location.name = self.location_map[location.location_id].name
          location.canEnter = location.read_write === 'w'
        })
        self.$set('location_permissions', locations)
        self.$set('locationalAccessLoading', false)
      })
    }
  }
}
