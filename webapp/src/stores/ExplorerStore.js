import _ from 'lodash'
import Reflux from 'reflux'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

var ExplorerStore = Reflux.createStore({
  listenables: [require('actions/ExplorerActions')],

  data: {
    locations: [],
    locationMap: [],
    campaign: {
      start: '',
      end: ''
    }
  },

  getInitialState: function () {
    return this.data
  },

  onGetLocations: function () {
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

  onUpdateDateRangePicker: function (key, value) {
    this.data.campaign[key] = value
    this.trigger(this.data)
  }
})

export default ExplorerStore
