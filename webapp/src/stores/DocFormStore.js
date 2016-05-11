import _ from 'lodash'
import api from 'utilities/api'
import Reflux from 'reflux'

var DocFormStore = Reflux.createStore({
  listenables: [require('actions/DocFormActions')],

  init () {
    this.data = {
      data_uri: null,
      config_options: [],
      uq_id_column: null,
      location_column: null,
      date_column: null,
      created_doc_id: null,
      doc_detail_meta: null,
      doc_is_refreshed: false,
      new_doc_title: null
    }
    api.docDetailType().then(response => {
      var doc_detail_types = _.indexBy(response.objects, 'name')
      this.data.doc_detail_meta = doc_detail_types
      this.trigger(this.data)
    })
  },

  onGetData (file, upload) {
    this.data.data_uri = upload.target.result

    api.uploadPost({
      docfile: upload.target.result,
      doc_title: file.name
    }).then(response => {
      this.data.config_options = response.objects.file_header.replace('"', '').split(',')
      this.data.created_doc_id = response.objects.id
      this.data.new_doc_title = response.objects.doc_title
      this.trigger(this.data)
    })
  },

  onSetDocConfig (config, config_type) {
    api.docDetailPost(config).then(response => {
      this.data[config_type] = response.objects.doc_detail_value
      this.trigger(this.data)
    })
  },

  onTransformUpload (document) {
    this.data.isRefreshing = true
    this.trigger(this.data)

    // api.sync_odk(data, null, {'cache-control': 'no-cache'}).then(res => {
    api.transformUpload(document, null, {'cache-control': 'no-cache'}).then(res => {
      if (res.objects) {
        this.data.doc_is_refreshed = true
        this.data.isRefreshing = true
        this.trigger(this.data)
      }
    }, res => {
      this.data.errorMessage = res.msg
      this.data.isRefreshing = false
      this.trigger(this.data)
    })
  },

  onSetOdkFormName (data) {
    api.sync_odk(data, null, {'cache-control': 'no-cache'}).then(res => {
      if (res.objects) {
        this.data.doc_obj = res.objects[0]
        this.data.created_doc_id = res.objects[0].id
        this.data.config_options = res.objects[0].file_header.replace('"', '').split(',')
        this.data.new_doc_title = res.objects[0].doc_title

        this.trigger(this.data)
      }
    }, res => {
      window.alert(res.msg)
    })
  }
})

export default DocFormStore
