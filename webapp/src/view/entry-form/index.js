import _ from 'lodash'
import d3 from 'd3'

import api from '../../data/api'
import Dropdown from '../../component/dropdown'
import flattenChildren from '../../data/transform/flattenChildren'
import treeify from '../../data/transform/treeify'

export default {
  template: require('./template.html'),

  data: function () {
    return {
      indicator_set_id: 2,
      indicator_sets: require('./structure/indicator_sets'),
      noEditableSets: false,
      loaded: false,
      includeSublocations: false,
      locations: [],
      indicators: [],
      pagination: {
        total_count: 0
      },
      table: {
        loading: false,
        columns: ['location', 'campaign'],
        rows: []
      },

      campaigns: [],
      campaign_id: null,
      campaign_office_id: null
    }
  },

  created: function () {
    // processing on indicator sets data
    _.forEach(this.indicator_sets, function (d) {
      // copy values for v-select:
      d.value = d.id
      d.text = d.title
    })
  },

  ready: function () {
    this.$watch('campaign_id', this.refreshlocationsDropdown)

    this.load()
  },

  attached: function () {
    var self = this

    // setup locations dropdown
    self._locations = new Dropdown({
      el: '#locations'
    })
    self._locations.$on('dropdown-value-changed', function (items) {
      self.locations = _.values(items)
    })

    this.$on('page-changed', function (data) {
      this.refresh(data)
    })
  },

  computed: {
    hasSelection: function () {
      return this.locations.length > 0
    }
  },

  methods: {
    load: function () {
      var self = this

      var makeMap = function (data) {
        if (data.objects) {
          return _.indexBy(data.objects, 'id')
        } else {
          return null
        }
      }

      var connectChildren = function (map, parent_id_key, children_key) {
        _.forIn(map, function (d) {
          // obj has parent_id?
          if (d[parent_id_key] !== undefined && d[parent_id_key] !== null) {
            // parent found?
            if (map[d[parent_id_key]]) {
              var parent = map[d[parent_id_key]]
              if (!parent[children_key]) { parent[children_key] = [] }
              parent[children_key].push(d)
            }
          }
        })
        return map
      }

      Promise.all([

        // locations data
        api.locations()
          .then(makeMap)
          .then(function (map) {
            // create array of children in each parent
            return connectChildren(map, 'parent_location_id', 'children')
          }),

        // indicators data
        api.indicators({ read_write: 'w' }, null, {'cache-control': 'no-cache'}).then(makeMap),

        // campaigns data
        api.campaign().then(function (data) {
          if (!data.objects) { return null }
          return data.objects
            .sort(function (a, b) {
              if (a.office === b.office) {
                return a.start_date > b.start_date ? -1 : 1
              }
              return a.office - b.office
            })
            .map(function (d) {
              d.text = d.slug
              d.value = d.id
              return d
            })
        })

      ]).then(function (allData) {
        self.$data.locationData = allData[0]
        self.$data.indicators = allData[1]
        self.$data.campaigns = allData[2]

        // set campaign id to first option
        self.$data.campaign_id = self.$data.campaigns[0].value
        self.$data.loaded = true

        self.filterIndicatorSets()
        self.refreshlocationsDropdown()
      })
    },

    refreshlocationsDropdown: function () {
      var self = this

      var campaign = _.find(self.$data.campaigns, function (d) { return d.id === parseInt(self.$data.campaign_id, 10) })

      var items = _.chain(self.$data.locationData)
              .filter(function (d) {
                return d.office_id === campaign.office_id
              })
              .map(function (d) {
                return {
                  'parent': d.parent_location_id,
                  'title': d.name,
                  'value': d.id
                }
              })
              .value()

      self._locations.items = items
      self._locations.itemTree = treeify(items, 'value')

      // if this campaign has a different office than the previous one, we have to clear the dropdown selection
      if (self.$data.campaign_office_id !== null && campaign.office_id !== self.$data.campaign_office_id) {
        self._locations.selection = {}
      }

      // set office id to track when the office changes
      self.$data.campaign_office_id = campaign.office_id
    },

    // filter list of indicator sets to exclude sets the user cannot edit at all
    filterIndicatorSets: function () {
      var self = this
      self.$data.indicator_sets = _.filter(self.$data.indicator_sets, function (s) {
        return _.find(s.indicators, function (i) {
          return i.id && self.$data.indicators[i.id] !== undefined
        })
      })
      self.$data.noEditableSets = self.$data.indicator_sets.length === 0
    },

    getFilteredIndicatorSet: function (indicatorSetId) {
      var self = this
      var indicatorSet = _.find(self.indicator_sets, function (d) { return d.id === parseInt(indicatorSetId, 10) })
      if (!indicatorSet) return null

      var filtered = _.clone(indicatorSet)
      filtered.indicators = []
      _.each(indicatorSet.indicators, function (row) {
        if (row.type === 'section-header') { // header
          // remove previous section header if no indicators are inlcuded under it
          if (filtered.indicators.length > 0 && filtered.indicators[filtered.indicators.length - 1].type === 'section-header') {
            filtered.indicators.splice(filtered.indicators.length - 1, 1)
          }
          filtered.indicators.push(row)
        } else { // indicator
          // filter out indicators the user cannot edit
          if (row.id && self.$data.indicators[row.id] !== undefined) {
            filtered.indicators.push(row)
          }
        }
      })
      // remove last row if empty section header
      if (filtered.indicators[filtered.indicators.length - 1].type === 'section-header') {
        filtered.indicators.pop()
      }

      return filtered
    },

    refresh: function () {
      var self = this

      if (!self.hasSelection) {
        return
      }

      var options = {
        campaign__in: parseInt(self.$data.campaign_id, 10),
        indicator__in: [],
        location__in: []
      }

      // add locations to request
      if (self.locations.length > 0) {
        // get all high risk children of selected locations
        _.forEach(self.locations, function (locationVue) {
          var location = self.$data.locationData[locationVue.value]
          options.location__in.push(location.id)

          if (self.includeSublocations) {
            // this will include all child locations:
            var children = flattenChildren(location, 'children', null, function () { return true }, 1)
            // this will include only high risk child locations
            // var children = flattenChildren(location, 'children', null, function (d) { return d.is_high_risk === true })
            if (children.length > 0) {
              options.location__in = options.location__in.concat(_.map(children, 'id'))
            }
          }
        })

        // make unique
        options.location__in = _.uniq(options.location__in)

        // sort locations
        options.location__in = options.location__in.sort(function (a, b) {
          var ra = self.$data.locationData[a]
          var rb = self.$data.locationData[b]
          // sort by location type first
          if (ra.location_type_id !== rb.location_type_id) {
            return ra.location_type_id - rb.location_type_id
          } else { // then name (alpha)
            return ra.name > rb.name ? 1 : -1
          }
        })
      }

      // add indicators to request
      var indicatorSet = self.getFilteredIndicatorSet(self.indicator_set_id)

      options.indicator__in = _(indicatorSet.indicators)
                    .filter(function (d) { return d.id })
                    .map(function (d) { return d.id })
                    .value()

      // define columns
      var columns = [
        {
          header: 'Indicator',
          type: 'label',
          headerClasses: 'medium-3'
        }
      ]
      // add location names as columns
      _.forEach(options.location__in, function (location_id) {
        columns.push({
          header: self.$data.locationData[location_id].name,
          type: 'value',
          key: location_id,
          children: null
        })
      })

      // cell formatters
      var numericFormatter = function (v) {
        return (isNaN(v) || _.isNull(v)) ? v : d3.format('n')(v)
      }

      _.defaults(options, self.pagination)

      // get datapoints from API
      self.table.loading = true
      var withSuccess = function (data) {
        // finished fetching data
        self.table.loading = false

        // arrange datapoints into an object of indicators > locations
        var byIndicator = {}
        data.objects.forEach(function (d) {
          if (!byIndicator[d.indicator_id]) { byIndicator[d.indicator_id] = {} }
          byIndicator[d.indicator_id][d.location_id] = d
        })

        // assemble data points into rows for table
        var rows = []
        _.each(indicatorSet.indicators, function (rowInfo) {
          var row = []

          if (rowInfo.type && rowInfo.type === 'section-header') { // section header row
            row.push({
              isEditable: false,
              type: 'label',
              value: rowInfo.title,
              class: 'section-header',
              colspan: columns.length
            })
          } else { // normal indicator row
            var indicator_id = rowInfo.id

            // add columns
            columns.forEach(function (column) {
              var cell = {
                isEditable: false,
                type: column.type
              }

              switch (column.type) {
                // editable value
                case 'value':
                  cell.isEditable = true
                  cell.format = numericFormatter
                  cell.classes = 'numeric'
                  cell.width = 80
                  if (byIndicator[indicator_id] && byIndicator[indicator_id][column.key]) {
                    cell.datapoint_id = byIndicator[indicator_id][column.key].datapoint_id
                    cell.value = byIndicator[indicator_id][column.key].value
                    cell.note = byIndicator[indicator_id][column.key].note
                  } else {
                    cell.datapoint_id = null
                    cell.value = null
                    cell.note = null
                  }
                  // tooltip
                  if (self.$data.locationData[column.key] && self.$data.indicators[indicator_id]) {
                    cell.tooltip = self.$data.indicators[indicator_id].name + ' value for ' + self.$data.locationData[column.key].name
                  } else {
                    cell.tooltip = null
                  }
                  // generate validation for values
                  cell.validateValue = function (newVal) {
                    var value, passed

                    if (_.isNull(newVal)) {
                      value = null
                      passed = true
                    } else {
                      value = parseFloat(newVal)
                      passed = !_.isNaN(value)
                    }
                    return { 'value': value, 'passed': passed }
                  }
                  // generate promise for submitting a new value to the API for saving
                  cell.buildSubmitPromise = function (newVal) {
                    var upsert_options = {
                      datapoint_id: cell.datapoint_id,
                      campaign_id: options.campaign__in,
                      indicator_id: indicator_id,
                      location_id: column.key,
                      value: parseFloat(newVal)
                    }
                    return api.datapointUpsert(upsert_options)
                  }
                  // callback to specifically handle response
                  cell.withResponse = function (response) {}
                  // callback to handle error
                  cell.withError = function (error) {
                    console.log(error)
                    if (error.msg && error.msg.message) { window.alert('Error: ' + error.msg.message) }
                    cell.hasError = true
                  }
                  break

                // indicator name
                case 'label':
                  cell.value = self.$data.indicators[indicator_id]
                    ? self.$data.indicators[indicator_id].name
                    : 'Missing info for indicator ' + indicator_id
                  cell.classes = 'label'
                  cell.width = 300
                  break
              }

              row.push(cell)
            })
          } // end normal indicator row

          rows.push(row)
        })

        self.table.rows = rows
        self.table.columns = columns
      }

      api.datapointsRaw(options).then(withSuccess, function (err) {
        self.table.loading = false
        console.error(err)
      })
    },

    showTooltip: function () {
      this.$broadcast('tooltip-show')
    },

    hideTooltip: function () {
      this.$broadcast('tooltip-hide')
    }
  }
}
