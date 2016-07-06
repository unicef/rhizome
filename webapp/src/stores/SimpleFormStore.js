import Reflux from 'reflux'
import api from 'utilities/api'
import _ from 'lodash'

import SimpleFormActions from 'actions/SimpleFormActions'

var SimpleFormStore = Reflux.createStore({
  data: {
    objectId: null,
    dataObject: null,
    componentData: {},
    formData: {},
    loading: true,
    saving: false,
    saveSuccess: false,
    indicators: []
  },

  listenables: [SimpleFormActions],

  getInitialState: function () {
    return this.data
  },

  onBaseFormSave: function (object_id, content_type, data_to_post) {
    console.log('BASE FORM SAVE')
    var self = this
    var fnLookup = {'indicator': api.post_indicator, 'indicator_tag': api.post_indicator_tag}
    var form_data =
    {'indicator': {
      'name': '',
      'short_name': '',
      'data_format': '',
      'description': '',
      'source_name': '',
      'bad_bound': '',
      'good_bound': ''
    },
      'indicator_tag': {'tag_name': ''}
    }

    var api_fn = fnLookup[content_type]

    let all_data = _.clone(data_to_post)
    all_data['id'] = object_id || -1

    Promise.all([
      api_fn(all_data)
    ])
      .then(_.spread(function (apiResponse) {
        self.data.formData = form_data[content_type]
        self.data.objectId = apiResponse.objects.id
        self.data.dataObject = apiResponse
        self.data.loading = false
        self.data.saveSuccess = true
        self.data.displayMsg = true
        self.data.message = 'Indicator is successfully created.'
        self.trigger(self.data)
      }), function (error) {
        self.data.formData = form_data[content_type]
        self.data.displayMsg = true
        self.data.dataObject = data_to_post
        self.data.saveSuccess = false
        self.data.message = error.msg
        self.data.loading = false
        self.trigger(self.data)
      })
  },

  onInitialize: function (object_id, content_type) {
    var self = this
    if (!object_id) {
      object_id = -1
    }

    self.data.objectId = object_id

    var fnLookup = {'indicator': api.indicators, 'indicator_tag': api.get_indicator_tag}
    var form_data =
    {'indicator': {
      'name': '',
      'short_name': '',
      'data_format': '',
      'description': '',
      'source_name': '',
      'bad_bound': '',
      'good_bound': ''
    },
      'indicator_tag': {'tag_name': ''}
    }
    var form_settings = {
      'indicator_tag': {
        'form': true,
        fields: {'tag_name': {type: 'string'}}
      },
      'indicator': {
        'form': true,
        fields: {
          'name': {type: 'string'},
          'short_name': {type: 'string'},
          'source_name': {type: 'string'},
          'bad_bound': {type: 'string'},
          'good_bound': {type: 'string'},
          'data_format': {
            type: 'select',
            settings: {options: [
                { value: 'pct', label: 'pct' },
                { value: 'bool', label: 'bool' },
                { value: 'int', label: 'int' },
                { value: 'class', label: 'class' }
            ]}
          },
          'description': {type: 'string'}
        }
      }
    }

    var api_fn = fnLookup[content_type]

    api_fn({ id: self.data.objectId }, null, { 'cache-control': 'no-cache' })
      .then(function (apiResponse) {
        self.data.formData = form_data[content_type]
        self.data.formSettings = form_settings[content_type]
        self.data.dataObject = apiResponse.objects[0]
        self.data.loading = false
        console.log('self.data', self.data)
        // code fails on trigger call
        self.trigger(self.data)
      })

    api.indicators(null, null, {'cache-control': 'no-cache'}).then(response => {
      self.data.indicators = _.pluck(_.sortBy(response.objects, 'name'), 'name')
      self.trigger(self.data)
    })
  },
  onAddIndicatorToTag: function (indicator_id, tag_id) {
    api.set_indicator_to_tag({ indicator_id: indicator_id, indicator_tag_id: tag_id }).then(function (response) {
      SimpleFormActions.refreshIndicators(tag_id)
    })
  },
  onAddTagToIndicator: function (indicator_id, tag_id) {
    api.set_indicator_to_tag({ indicator_id: indicator_id, indicator_tag_id: tag_id }).then(function (response) {
      SimpleFormActions.refreshTags(indicator_id)
    })
  },

  onRemoveTagFromIndicator: function (indicator_id, id) {
    api.remove_indicator_from_tag({ id: id }).then(function (response) {
      SimpleFormActions.refreshTags(indicator_id)
    })
  },

  onAddCalculationToIndicator: function (indicator_id, component_id, calculation) {
    api.set_calc_to_indicator({
      indicator_id: indicator_id,
      indicator_component_id: component_id,
      calculation: calculation
    }).then(function (response) {
      SimpleFormActions.refreshCalculation(indicator_id)
    })
  },

  onRemoveCalculationFromIndicator: function (indicator_id, id) {
    api.remove_calc_from_indicator({ id: id }).then(function (response) {
      SimpleFormActions.refreshCalculation(indicator_id)
    })
  },

  onRemoveIndicatorFromTag: function (id, tagId) {
    api.remove_indicator_from_tag({ id: id }).then(function (response) {
      SimpleFormActions.refreshIndicators(tagId)
    })
  },

  onRefreshTags: function (indicator_id) {
    var self = this
    api.indicator_to_tag({ indicator_id: indicator_id }, null, {'cache-control': 'no-cache'}).then(function (indicator_to_tag) {
      var indicatorTags = _.map(indicator_to_tag.objects, function (row) {
        return {'id': row.id, displayId: row.id, 'display': row.indicator_tag__tag_name}
      })

      self.data.componentData['indicator_tag'].componentRows = indicatorTags
      self.trigger(self.data)
    })
  },

  onRefreshCalculation: function (indicator_id) {
    var self = this
    api.indicator_to_calc({ indicator_id: indicator_id }, null, {'cache-control': 'no-cache'}).then(function (indicator_to_calc) {
      var indicatorCalcList = _.map(indicator_to_calc.objects, function (row) {
        return {
          'id': row.id,
          displayId: row.indicator_component_id,
          'display': row.calculation + ' - ' + row.indicator_component__short_name
        }
      })

      self.data.componentData['indicator_calc'].componentRows = indicatorCalcList
      self.trigger(self.data)
    })
  },

  onRefreshIndicators: function (tagId) {
    var self = this
    api.indicator_to_tag({ indicator_tag_id: tagId }, null, {'cache-control': 'no-cache'}).then(function (tags) {
      var indicatorTags = _.map(tags.objects, function (row) {
        return {
          'id': row.id, displayId: row.id, 'display': row.indicator__short_name
        }
      })

      self.data.componentData['indicator'].componentRows = indicatorTags
      self.trigger(self.data)
    })
  },

  onInitIndicatorToCalc: function (indicatorId) {
    var self = this

    Promise.all([
      api.indicator_to_calc({ indicator_id: indicatorId }, null, {'cache-control': 'no-cache'}),
      api.indicatorsTree()
    ])
      .then(_.spread(function (indicatorToCalc, indicators) {
        var allIndicators = _(indicators.objects).sortBy('title').value()

        var indicatorCalcList = _.map(indicatorToCalc.objects, function (row) {
          return {
            id: row.id,
            displayId: row.indicator_component_id,
            display: row.calculation + ' - ' + row.indicator_component__short_name
          }
        })

        self.data.componentData['indicator_calc'] = {'componentRows': indicatorCalcList, 'dropDownData': allIndicators}
        self.data.loading = false
        self.trigger(self.data)
      }))
  },

  onInitIndicatorToTag: function (indicatorId) {
    var self = this

    console.log('onInitIndicatorToTag  indicatorId ID: ', indicatorId)

    Promise.all([
      api.indicator_to_tag({ indicator_id: indicatorId }, null, {'cache-control': 'no-cache'}),
      api.tagTree({}, null, {'cache-control': 'no-cache'})
    ])
      .then(_.spread(function (indicatorToTag, TagTree) {
        var allTags = TagTree.objects
        var indicatorTags = _.map(indicatorToTag.objects, function (row) {
          return {'id': row.id, displayId: row.id, 'display': row.indicator_tag__tag_name}
        })

        self.data.componentData['indicator_tag'] = {'componentRows': indicatorTags, 'dropDownData': allTags}
        self.data.loading = false
        self.trigger(self.data)
      }))
  },
  onInitTagToIndicator: function (tagId) {
    var self = this

    Promise.all([
      api.indicator_to_tag({ indicator_tag_id: tagId }, null, {'cache-control': 'no-cache'}),
      api.indicatorsTree({}, null, {'cache-control': 'no-cache'})
    ])
      .then(_.spread(function (tags, indicators) {
        var indicatorsData = _(indicators.objects).sortBy('title').value()
        var indicatorTags = _.map(tags.objects, function (row) {
          return {'id': row.id, displayId: row.id, 'display': row.indicator__short_name}
        })

        self.data.componentData['indicator'] = {'componentRows': indicatorTags, 'dropDownData': indicatorsData}
        self.data.loading = false
        self.trigger(self.data)
      }))
  }

})

export default SimpleFormStore
