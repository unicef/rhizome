'use strict'

var Reflux = require('reflux')
var api = require('data/api')
var _ = require('lodash')

var SimpleFormActions = require('actions/SimpleFormActions')

var SimpleFormStore = Reflux.createStore({
  data: {
    objectId: null,
    dataObject: null,
    componentData: {},
    formData: {},
    loading: true,
    saving: false,
    saveSuccess: false
  },

  listenables: [SimpleFormActions],

  getInitialState: function () {
    return this.data
  },

  onBaseFormSave: function (object_id, content_type, data_to_post) {
    var self = this
    var fnLookup = {'indicator': api.post_basic_indicator, 'indicator_tag': api.post_indicator_tag}
    var api_fn = fnLookup[content_type]

    var id_to_post = object_id || -1

    data_to_post['id'] = id_to_post

    Promise.all([
      api_fn(data_to_post)
    ])
      .then(_.spread(function (apiResponse) {
        self.data.formData = apiResponse.meta.form_data
        self.data.objectId = apiResponse.objects.id
        self.data.dataObject = apiResponse
        self.data.loading = false
        self.data.saveSuccess = true
        self.trigger(self.data)
      }))
  },

  onInitialize: function (object_id, content_type) {
    var self = this
    if (!object_id) {
      var object_id = -1
    }

    self.data.objectId = object_id

    var fnLookup = {'indicator': api.get_basic_indicator, 'indicator_tag': api.get_indicator_tag}
    var api_fn = fnLookup[content_type]

    Promise.all([
      api_fn({ id: self.data.objectId }, null, { 'cache-control': 'no-cache' })
    ])
      .then(_.spread(function (apiResponse) {
        self.data.formData = apiResponse.meta.form_data
        self.data.dataObject = apiResponse.objects[0]
        self.data.loading = false
        self.trigger(self.data)
      }))
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

  onAddCalculationToIndicator: function (indicator_id, component_id, typeInfo) {
    api.set_calc_to_indicator({
      indicator_id: indicator_id,
      component_id: component_id,
      typeInfo: typeInfo
    }).then(function (response) {
      SimpleFormActions.refreshCalculation(indicator_id)
    })
  },

  onRemoveCalculationFromIndicator: function (indicator_id, id) {
    api.remove_calc_from_indicator({ id: id }).then(function (response) {
      SimpleFormActions.refreshCalculation(indicator_id)
    })
  },

  deleteTagFromIndicator: function (data) {},

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

  onInitIndicatorToCalc: function (indicator_id) {
    var self = this

    Promise.all(
      [api.indicator_to_calc({ indicator_id: indicator_id }, null, {'cache-control': 'no-cache'}),
        api.indicatorsTree()]
    )
      .then(_.spread(function (indicator_to_calc, indicators) {
        var allIndicators = _(indicators.objects).sortBy('title').value()

        var indicatorCalcList = _.map(indicator_to_calc.objects, function (row) {
          return {
            'id': row.id,
            displayId: row.indicator_component_id,
            'display': row.calculation + ' - ' + row.indicator_component__short_name
          }
        })

        self.data.componentData['indicator_calc'] = {'componentRows': indicatorCalcList, 'dropDownData': allIndicators}
        self.data.loading = false
        self.trigger(self.data)
      }))
  },

  onInitIndicatorToTag: function (indicator_id) {
    var self = this

    Promise.all(
      [api.indicator_to_tag({ indicator_id: indicator_id }, null, {'cache-control': 'no-cache'}),
        api.tagTree({}, null, {'cache-control': 'no-cache'})] // cache_control
    )
      .then(_.spread(function (indicator_to_tag, tag_tree) {
        var allTags = tag_tree.objects
        var indicatorTags = _.map(indicator_to_tag.objects, function (row) {
          return {'id': row.id, displayId: row.id, 'display': row.indicator_tag__tag_name}
        })

        self.data.componentData['indicator_tag'] = {'componentRows': indicatorTags, 'dropDownData': allTags}
        self.data.loading = false
        self.trigger(self.data)
      }))
  }

})

module.exports = SimpleFormStore
