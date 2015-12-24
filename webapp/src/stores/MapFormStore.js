import Reflux from 'reflux'
import api from 'data/api'

import MapFormActions from 'actions/MapFormActions'

var MapFormStore = Reflux.createStore({
  listenables: MapFormActions,
  data: {
    modalIsOpen: false,
    content_type: null,
    master_object_id: null,
    master_object_name: null,
    source_object_code: null
  },

  getInitialState: function () {
    return this.data
  },

  onGetSourceMap: function (id) {
    api.get_source_object_map(id, null, {'cache-control': 'no-cache'})
      .then(response => {
        this.trigger({
          modalIsOpen: true,
          content_type: response.objects[0].content_type,
          master_object_id: response.objects[0].mapped_by_id,
          source_object_code: response.objects[0].source_object_code
        })
      })
  },

  onUpdateMetaMap: function (info) {
    api.post_source_object_map(info)
      .then(response => {
        this.trigger({
          master_object_id: response.objects.mapped_by_id,
          master_object_name: response.objects.master_object_name
        })
      })
  },

  onClear: function () {
    this.trigger({
      modalIsOpen: false,
      content_type: null
    })
  },

  getIndicators: function () {
    return api.indicatorsTree().then(indicators => {
      return indicators.objects
    })
  }
})

export default MapFormStore
