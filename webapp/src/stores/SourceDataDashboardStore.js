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

      api.sync_odk(data).then(res => {
        if (res.objects.id) {
          window.location = '/datapoints/dashboards/edit/' + res.objects.id
        } else {
          window.alert('There was an error saving your chart')
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
