'use strict'

import _ from 'lodash'
import api from 'data/api'
import Reflux from 'reflux'

var DocFormStore = Reflux.createStore({
  listenables: [require('actions/DocFormActions')],

  init: function () {
    this.data = {
      data_uri: null,
      config_options: [],
      uq_id_column: null,
      location_column: null,
      campaign_column: null,
      created_doc_id: null,
      doc_detail_meta: null,
      doc_is_refreshed: false,
      new_doc_title: null
    }
  },

  onGetData: function (file, upload) {
    var self = this
    self.data.data_uri = upload.target.result

    api.uploadPost({
      docfile: upload.target.result,
      doc_title: file.name
    }).then(function (response) {
      var new_doc_obj = response.objects
      self.data.config_options = new_doc_obj.file_header.replace('"', '').split(',')
      self.data.created_doc_id = new_doc_obj.id
      self.data.new_doc_title = new_doc_obj.doc_title
      self.trigger(self.data)
    })

    api.docDetailType().then(function (response) {
      var doc_detail_types = _.indexBy(response.objects, 'name')
      self.data.doc_detail_meta = doc_detail_types
      self.trigger(self.data)
    })
  },

  onSetDocConfig: function (config, config_type) {
    var self = this
    api.docDetailPost(config).then(function (response) {
      self.data[config_type] = response.objects.doc_detail_value
      self.trigger(self.data)
    })
  },

  onTransformUpload: function (document) {
    var self = this
    api.transformUpload(document, null, {'cache-control': 'no-cache'})
      .then(function (response) {
        self.data.doc_is_refreshed = true
        self.trigger(self.data)
      })
  }
})

module.exports = DocFormStore
