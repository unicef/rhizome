'use strict'

import api from 'data/api'
import Reflux from 'reflux'
import parseSchema from 'ufadmin/utils/parseSchema'

var ReviewTableStore = Reflux.createStore({
  listenables: [require('actions/ReviewTableActions')],

  init: function () {
    this.data = {
      data: null,
      schema: null,
      query: {},
      loading: false
    }
  },

  onGetData: function (request, fields, docTab) {
    var self = this
    if (docTab === 'viewraw') {
      api.submission(request, null, {'cache-control': 'no-cache'}).then(response => {
        self.data.schema = parseSchema(fields)
        self.data.data = response.objects
        self.trigger(self.data)
      })
    } else if (docTab === 'doc_index') {
      api.source_doc(request, null, {'cache-control': 'no-cache'}).then(response => {
        self.data.schema = parseSchema(fields)
        self.data.data = response.objects
        self.trigger(self.data)
      })
    } else if (docTab === 'mapping') {
      api.docMap(request, null, {'cache-control': 'no-cache'}).then(response => {
        self.data.schema = parseSchema(fields)
        self.data.data = response.objects
        self.trigger(self.data)
      })
    } else if (docTab === 'validate') {
      api.docDatapoint(request, null, {'cache-control': 'no-cache'}).then(response => {
        self.data.schema = parseSchema(fields)
        self.data.data = response.objects
        self.trigger(self.data)
      })
    } else {
      // results
      api.docResults(request, null, {'cache-control': 'no-cache'}).then(response => {
        self.data.schema = parseSchema(fields)
        self.data.data = response.objects
        self.trigger(self.data)
      })
    }
  },

  onGetIndicators: function () {
    var self = this
    api.indicatorsTree().then(indicators => {
      self.data.indicators = indicators
      self.trigger(self.data)
    })
  }
})

module.exports = ReviewTableStore
