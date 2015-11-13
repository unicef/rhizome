'use strict'
import Reflux from 'reflux'
import _ from 'lodash'

import api from 'data/api'
import GroupFormActions from 'actions/GroupFormActions'

module.exports = Reflux.createStore({
  data: {
    groupId: null,
    groupName: null,
    indicatorList: [],
    indicatorsSelected: [],
    loading: true,
    saving: false
  },
  listenables: [ GroupFormActions ],
  getInitialState: function () {
    return this.data
  },
  onInitialize: function (group_id) {
    var self = this

    self.data.groupId = group_id

    // always get the indicator tree
    api.indicatorsTree().then(function (indicators) {
      // process indicators
      self._indicatorIndex = _.indexBy(indicators.flat, 'id')
      self.data.indicatorList = _(indicators.objects)
        .sortBy('title')
        .value()

      // updating existing group? need to get more data
      if (self.data.groupId) {
        Promise.all([
          api.groups(),
          api.group_permissions({ group: self.data.groupId }, null, { 'cache-control': 'no-cache' })
        ])
        .then(_.spread(function (groups, groupPermissions) {
          // find current group
          var g = _.find(groups.objects, function (d) { return d.id === self.data.groupId })
          self.data.groupName = g.name

          // select current permissions
          _.each(groupPermissions.objects, function (d) {
            if (d.indicator_id) {
              self.data.indicatorsSelected.push(self._indicatorIndex[d.indicator_id])
            }
          })

          self.data.loading = false
          self.trigger(self.data)
        }))
      } else { // creating new group
        self.data.loading = false
        self.trigger(self.data)
      }
    })
  },
  onAddIndicatorSelection: function (value) {
    var self = this
    api.group_permissionUpsert({ group_id: self.data.groupId, indicator_id: value })
      .then(function (response) {
        self.data.indicatorsSelected.push(self._indicatorIndex[value])
        self.trigger(self.data)
      })
  },
  onRemoveIndicatorSelection: function (value) {
    var self = this
    api.group_permissionUpsert({ group_id: self.data.groupId, indicator_id: value, id: '' })
      .then(function (response) {
        _.remove(self.data.indicatorsSelected, { id: value })
        self.trigger(self.data)
      })
  },
  onUpdateName: function (name) {
    this.data.groupName = name
    this.trigger(this.data)
  },
  onSaveGroupForm: function () {
    var self = this
    self.data.saving = true
    var post = {
      name: self.data.groupName
    }
    if (self.data.groupId) post.id = self.data.groupId
    api.groupUpsert(post).then(function (response) {
      if (response.objects.new_id) {
        self.data.groupId = response.objects.new_id
      }
      setTimeout(function () {
        self.data.saving = false
        self.trigger(self.data)
      }, 500)
      self.trigger(self.data)
    })
  }
})
