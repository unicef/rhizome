import _ from 'lodash'
import d3 from 'd3'
import moment from 'moment'
import React from 'react'

import api from '../../data/api'
import Dropdown from '../../component/dropdown'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import List from 'component/list/List.jsx'
import DateRangePicker from 'component/DateTimePicker.jsx'

export default {
  template: require('./template.html'),

  data: function () {
    return {
      locations: [],
      indicators: [],
      indicatorsForList: [],
      pagination: {
        limit: 20,
        offset: 0,
        total_count: 0
      },
      table: {
        loading: false,
        columns: ['location', 'campaign'],
        rows: []
      },
      campaign: {
        start: '',
        end: ''
      }
    }
  },

  attached: function () {
    var self = this

    this._locations = new Dropdown({
      el: '#locations',
      source: (params) => api.locations(params, null, {'cache-control': 'no-cache'}),
      mapping: {
        'parent_location_id': 'parent',
        'name': 'title',
        'id': 'value'
      }
    })

    this._locations.$on('dropdown-value-changed', function (items) {
      self.locations = _.values(items)
    })

    this.$on('page-changed', function (data) {
      this.refresh(data)
    })

    // render indicator dropdown
    api.indicatorsTree()
      .then(function (response) {
        var ddProps = {
          indicators: response.objects,
          text: 'Choose Indicators',
          sendValue: self.updateIndicatorSelection
        }
        self.indicatorMap = _.indexBy(response.flat, 'id')
        self.indicatorDropdown = React.render(React.createElement(IndicatorDropdownMenu, ddProps), document.getElementById('indicatorSelector'))
      })

    var dateRangePickerProps = {
      start: self.campaign.start,
      end: self.campaign.end,
      sendValue: self.updateDateRangePicker
    }
    React.render(React.createElement(DateRangePicker, dateRangePickerProps), document.getElementById('dateRangePicker'))
  },

  computed: {
    hasSelection: function () {
      return this.locations.length > 0 && this.indicators.length > 0
    }
  },

  methods: {
    renderIndicatorList: function () {
      var listProps = {
        items: this.indicators,
        removeItem: this.removeIndicatorFromSelection
      }
      React.render(React.createElement(List, listProps), document.getElementById('indicatorList'))
    },

    updateIndicatorSelection: function (id) {
      this.indicators.push(this.indicatorMap[id])
      this.renderIndicatorList()
    },

    removeIndicatorFromSelection: function (id) {
      _.remove(this.indicators, function (d) {
        return d.id === id
      })
      this.renderIndicatorList()
    },

    updateDateRangePicker: function (key, value) {
      this.campaign[key] = value
    },

    refresh: function (pagination) {
      if (!this.hasSelection) {
        return
      }

      var self = this

      var locationNames = _.indexBy(this.locations, 'value')
      var locations = _.map(this.locations, 'value')
      var options = { indicator__in: [] }
      var columns = [{
        prop: 'location',
        display: 'location',
        format: function (v) {
          return locationNames[v].title
        }
      }, {
        prop: 'campaign',
        display: 'Campaign'
      }]

      if (locations.length > 0) {
        options.location__in = locations
      }

      if (this.campaign.start) {
        options.campaign_start = this.campaign.start
      }

      if (this.campaign.end) {
        options.campaign_end = this.campaign.end
      }

      this.indicators.forEach(function (indicator) {
        options.indicator__in.push(indicator.value)
        columns.push({
          prop: indicator.value,
          display: indicator.title,
          classes: 'numeric',
          format: function (v) {
            if (_.isFinite(v)) {
              var fmt = d3.format('n')
              if (Math.abs(v) < 1 && v !== 0) {
                fmt = d3.format('.4f')
              }

              return fmt(v)
            }

            return ''
          }
        })
      })

      _.defaults(options, pagination, _.omit(this.pagination, 'total_count'))

      this.table.rows = []
      this.table.columns = columns
      this.table.loading = true

      api.datapoints(options).then(function (data) {
        self.table.loading = false

        _.assign(self.pagination, _.pick(data.meta, 'limit', 'offset', 'total_count'))

        if (!data.objects || data.objects.length < 1) {
          return
        }

        var datapoints = data.objects.map(function (v) {
          var d = _.pick(v, 'location')

          d.campaign = moment(v.campaign.start_date).format('MMM YYYY')

          v.indicators.forEach(function (ind) {
            d[ind.indicator] = ind.value
          })

          return d
        })

        self.table.rows = datapoints
      })
    },

    download: function () {
      if (!this.hasSelection) {
        return
      }

      this.downloading = true

      var indicators = _.map(this.indicators, 'value')
      var locations = _.map(this.locations, 'value')
      var query = {
        'format': 'csv'
      }

      if (indicators.length < 1) {
        this.$data.src = ''
        return
      }

      query.indicator__in = indicators
      if (locations.length > 0) {
        query.location__in = locations
      }

      if (this.campaign.start) {
        query.campaign_start = this.campaign.start
      }

      if (this.campaign.end) {
        query.campaign_end = this.campaign.end
      }

      this.$set('src', api.datapoints.toString(query))
    },

    previous: function () {
      if (this.pagination.offset < 1) {
        return
      }

      this.pagination.offset = Math.max(0, this.pagination.offset - this.pagination.limit)
      this.refresh()
    },

    next: function () {
      this.pagination.offset += this.pagination.limit
      this.refresh()
    }
  }
}
