import api from 'utilities/api'
import Reflux from 'reflux'

var SourceDataStore = Reflux.createStore({
  listenables: [require('actions/SourceDataActions')],

  init: function () {
    var self = this
    self.data = {}

    let currentPath = window.location.pathname
    let cleanPath = currentPath.replace('/source-data/', '')
    let urlParams = cleanPath.split('/')
    let doc_tab = 'doc_index'
    let doc_id = null


    if (urlParams.length === 2) {
      doc_tab = urlParams[0],
      doc_id = urlParams[1],
      this.getDocObj(doc_id)
    }
    self.trigger(self.data)
  },

  getInitialState () {
    return {
      tableDef: this.getTableDef()
    }
    return initialState
  },

  getDocObj: function (doc_id) {
    var self = this
      api.source_doc({id: doc_id}).then(function (response) {
      self.data.doc_obj = response.objects[0]
      self.data.file_type = response.objects[0].file_type
      self.trigger(self.data)
    })
  },

  getTableDef: function () {
    var self = this
    console.log('SourceDataStore - getTableDef: ', self)

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
        'fields': ['id', 'doc_title','file_type', 'created_at', 'edit_link'],
        'header': ['id', 'doc_title','file_type', 'created_at', 'edit_link'],
        'search_fields': ['id', 'doc_title']
      },
      'mapped': {
        'display_name': 'Meta Data ( Mapped )',
        'data_fn': api.docMapped,
        'fields': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'header': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'search_fields': ['content_type', 'source_object_code', 'master_object_name']
      },
      'un-mapped': {
        'display_name': 'Meta Data ( Mapped )',
        'data_fn': api.docToMap,
        'fields': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'header': ['content_type', 'source_object_code', 'master_object_name', 'edit_link'],
        'search_fields': ['content_type', 'source_object_code', 'master_object_name']
      },
      'date_results': {
        'data_fn': api.dateDocResults,
        'fields': ['indicator__id', 'indicator__short_name', 'location__name', 'data_date', 'value'],
        'fields': ['indicator__id', 'indicator__short_name', 'location__name', 'data_date', 'value'],
        'search_fields': ['indicator_id', 'indicator__short_name', 'location__name', 'campaign__name']
      },
      'campaign_results': {
        'data_fn': api.campaignDocResults,
        'fields': ['indicator__id', 'indicator__short_name', 'location__name', 'campaign__name', 'value'],
        'fields': ['indicator__id', 'indicator__short_name', 'location__name', 'campaign__name', 'value'],
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
