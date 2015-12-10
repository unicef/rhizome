import api from 'data/api'
import Reflux from 'reflux'

var DocOverviewStore = Reflux.createStore({
  listenables: [require('actions/DocOverviewActions')],

  init: function () {
    this.data = {
      doc_id: null,
      doc_title: null,
      doc_detail_types: null,
      doc_deets: null
    }
  },

  onGetDocDetails: function (document_id) {
    var self = this
    api.docDetail({document_id:document_id})
      .then(response => {
        self.data.doc_deets = response.objects
        self.trigger(self.data)
      })
  },

  onRefreshMaster: function (document_id) {
    var self = this
    self.data.isRefreshing = true
    self.trigger(self.data)

    api.refresh_master(document_id, null, {'cache-control': 'no-cache'})
      .then(function (response) {
        self.data.doc_deets = response.objects
        self.data.isRefreshing = false
        self.trigger(self.data)
      }, function (response) {
        self.data.isProcessing = false
        self.trigger(self.data)
      })
  },

  onQueueReprocess: function (document_id) {
    var self = this
    self.data.isProcessing = true
    self.trigger(self.data)

    api.queue_reprocess(document_id, null, {'cache-control': 'no-cache'})
      .then(function (response) {
        self.data.doc_deets = response.objects
        self.data.isProcessing = false
        self.trigger(self.data)
      }, function (response) {
        self.data.isProcessing = false
        self.trigger(self.data)
      })
  }
})

export default DocOverviewStore
