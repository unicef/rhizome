import api from 'data/api'
import Reflux from 'reflux'

var SourceDataDashboardStore = Reflux.createStore({
  listenables: [require('actions/SourceDataDashboardActions')],

  init: function () {
    this.data = {
      doc_obj: null
    }
  },

  onSetOdkFormName: function (data) {
      api.sync_odk(data, null, {'cache-control':'no-cache'}).then(res => {
        if (res.objects) {
          self.data.doc_obj = response.objects[0]
        }
        }, res => {
        window.alert(res.msg)
      })
  },

  onGetDocObj: function (doc_id) {
    var self = this
    api.source_doc({ id: doc_id }).then(function (response) {
      self.data.doc_obj = response.objects[0]
      self.trigger(self.data)
    })
  }
})

export default SourceDataDashboardStore
