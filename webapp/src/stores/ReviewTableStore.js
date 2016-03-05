import api from 'data/api'
import Reflux from 'reflux'
import parseSchema from 'components/organisms/ufadmin/utils/parseSchema'

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
    const tabMapping = {
      'viewraw': api.submission,
      'doc_index': api.source_doc,
      'mapping': api.docMap,
      'validate': api.docDatapoint,
      'results': api.docResults
    }
    tabMapping[docTab](request, null, {'cache-control': 'no-cache'}).then(response => {
      this.data.schema = parseSchema(fields)
      this.data.data = response.objects
      this.trigger(this.data)
    })
  },

  onGetIndicators: function () {
    api.indicatorsTree().then(indicators => {
      this.data.indicators = indicators
      this.trigger(this.data)
    })
  }
})

export default ReviewTableStore
