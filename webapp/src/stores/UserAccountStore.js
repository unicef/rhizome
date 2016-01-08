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
      })
  },

  onAddLocations: function (id) {
    this.data.locationSelected.push(this.data.locationMap[id])
    this.trigger(this.data)
  },

  onRemoveLocation: function (id) {
    _.remove(this.data.locationSelected, {id: id})
    this.trigger(this.data)
  }
})

export default UserAccountStore
