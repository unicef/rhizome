import Reflux from 'reflux'
import _ from 'lodash'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

var UserAccountStore = Reflux.createStore({
  listenables: [require('actions/UserAccountActions')],

  data: {
    locations: [],
    locationMap: [],
    locationSelected: []
  },

  getInitialState: function () {
    return this.data
  },

  onGetLocations: function (userId) {
    api.locations()
      .then(response => {
        this.data.locations = _(response.objects)
          .map(location => {
            return {
              'title': location.name,
              'value': location.id,
              'parent': location.parent_location_id
            }
          })
          .sortBy('title')
          .reverse()
          .thru(_.curryRight(treeify)('value'))
          .map(ancestryString)
          .value()

        this.data.locationMap = _.indexBy(response.objects, 'id')
        this.trigger(this.data)

        this._getLocationAccess(userId)
      })
  },

  onSetLocationAccess: function (userId, locationId) {
    var self = this
    api.set_location_responsibility({ user_id: userId, location_id: locationId }).then(function () {
      self._getLocationAccess(userId)
    })
  },

  _getLocationAccess: function (userId) {
    let self = this
    api.location_responsibility({ user_id: userId }, null, {'cache-control': 'no-cache'}).then(function (data) {
      let locations = data.objects
      if (locations && locations.length > 0) {
        self.data.locationSelected[0] = self.data.locationMap[locations[0].top_lvl_location_id]
      }
      self.trigger(self.data)
    })
  }
})

export default UserAccountStore
