import api from 'utilities/api'
import Reflux from 'reflux'

var SourceDataStore = Reflux.createStore({
  listenables: [require('actions/SourceDataActions')],

  init: function () {
    var self = this

    self.data = {
      docObj: null,
      docTab: 'doc_index',
      tableDef: this.getTableDef()
    }
    self.trigger(self.data)
  },

  getInitialState () {
    var initialState = {
      tableDef: this.getTableDef(),
      doc_id: null,
      doc_tab: 'doc_index'
    }
    return initialState
  },

  onGetDocObj: function (doc_id) {
    var self = this
    api.source_doc({ id: doc_id }).then(function (response) {
      self.data.doc_obj = response.objects[0]
      self.trigger(self.data)
    })
  },

  getTableDef: function () {
    return {
      'viewraw': {
        'meta_fn': api.submissionMeta,
        'data_fn': api.submission,
        'fields': ['id', 'location_code', 'campaign_code', 'edit_link'],
        'header': ['id', 'location_code', 'campaign_code', 'edit_link'],
        'search_fields': ['id', 'location_code', 'campaign_code']
      },
      'doc_index': {
        'data_fn': api.source_doc,
        'fields': ['id', 'doc_title', 'created_at', 'edit_link'],
        'header': ['id', 'doc_title', 'created_at', 'edit_link'],
        'search_fields': ['id', 'doc_title']
      },
      'meta-data': {
        'data_fn': api.docMap,
        'fields': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'header': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'search_fields': ['content_type', 'source_object_code', 'master_object_name']
      },
      'results': {
        'data_fn': api.docResults,
        'fields': ['indicator_id', 'indicator__short_name', 'location__name', 'campaign__name', 'value'],
        'header': ['indicator_id', 'indicator__short_name', 'location__name', 'campaign__name', 'value'],
        'search_fields': ['indicator_id', 'indicator__short_name', 'location__name', 'campaign__name']
      }
      // 'errors': {
      //   'data_fn': api.docMap,
      //   'fields': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
      //   'header': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
      //   'search_fields': ['content_type', 'source_object_code', 'master_object_name']
      // }
    }
  }
})

export default SourceDataStore
