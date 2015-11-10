'use strict'

var _ = require('lodash')
var api = require('data/api')
var Reflux = require('reflux')

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

  onGetDocDetailTypes: function () {
    var self = this
    api.docDetailType()
      .then(response => {
        self.data.doc_detail_types = response.objects
        self.trigger(self.data)
      })
  },

  onRefreshMaster: function (document) {
    var self = this
    self.data.isRefreshing = true
    self.trigger(self.data)

    api.refresh_master(document, null, {'cache-control': 'no-cache'})
      .then(function (response) {
        self.data.doc_deets = response.objects
        self.data.isRefreshing = false
        self.trigger(self.data)
      }, function (response) {
        self.data.isProcessing = false
        self.trigger(self.data)
      })
  },

  onQueueReprocess: function (document) {
    var self = this
    self.data.isProcessing = true
    self.trigger(self.data)

    api.queue_reprocess(document, null, {'cache-control': 'no-cache'})
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

module.exports = DocOverviewStore
