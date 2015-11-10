/* global window */
'use strict'

var _ = require('lodash')
var d3 = require('d3')
var moment = require('moment')
var page = require('page')
var React = require('react')

var api = require('data/api')
var util = require('util/data')

var Chart = require('component/Chart.jsx')

var RANGE_ORDER = {
  'bad': 0,
  'ok': 1,
  'okay': 1,
  'good': 2
}

/**
 * @private
 * Return true if indicator is an object with an array of bound_json.
 */
function _hasBounds (indicator) {
  return _.isObject(indicator) && !_.isEmpty(indicator.bound_json)
}

/**
 * @private
 * Return an array of indicator objects sorted by order.
 *
 * @param {Object} indicators Response object from indicators API
 * @param {Array} order An array of indicator IDs that defines the order of
 *   the returned array
 */
function _heatmapColumns (indicators, order) {
  return _(indicators.objects)
    .filter(_hasBounds)
    .sortBy(function (indicator) {
      return order.indexOf(indicator.id)
    })
    .value()
}

/**
 * @private
 * Convert 'NULL' strings on a bound definition to +/- Infinity
 *
 * Create a new object with non-number properties replaced by +/- Infinity.
 * mn_val is replaced by -Infinity, and mx_val is replaced by Infinity, if
 * either has a non-numeric property.
 *
 * @param {Object} bound A target range definition for an indicator
 */
function _openBounds (bound) {
  var lower = _.isNumber(bound.mn_val) ? bound.mn_val : -Infinity
  var upper = _.isNumber(bound.mx_val) ? bound.mx_val : Infinity

  return _.assign({}, bound, {
    mn_val: lower,
    mx_val: upper
  })
}

function _getBoundOrder (bound) {
  return _.get(RANGE_ORDER, bound.bound_name, Infinity)
}

module.exports = {
  template: require('./district.html'),

  data: function () {
    return {
      campaign: null,
      columns: [],
      location: null,
      locations: {},
      series: [],
      showEmpty: false
    }
  },

  methods: {
    error: function () {},

    load: function () {
      this.loading = true

      if (!(this.campaign && this.location)) {
        return
      }

      var indicators = [
        475, 166, 164, 167, 165, // Missed Children
        222, // Microplans
        187, 189, // Conversions
        // FIXME: Transit points in place and with SM
        178, 228, 179, 184, 180, 185, 230, 226, 239, // Capacity to Perform
        194, 219, 173, 172, // Supply
        245, 236, 192, 193, 191, // Polio+
        174, // Access plan
        442, 443, 444, 445, 446, 447, 448, 449, 450 // Inaccessibility
      ]

      var datapoints = api.datapoints({
        parent_location__in: this.location.id,
        admin_level: 2,
        indicator__in: indicators,
        campaign_start: moment(this.campaign.start_date).format('YYYY-MM-DD'),
        campaign_end: moment(this.campaign.end_date).format('YYYY-MM-DD')
      })

      console.log(datapoints)
      console.log('DATAPOINTS APOVE')

      var columns = api.indicators({ id__in: indicators }, null, {'cache-control': 'no-cache'})
        .then(_.partialRight(_heatmapColumns, indicators))

      var self = this

      Promise.all([columns, datapoints])
        .then(function (data) {
          var columns = data[0]

          // Create a function for extracting and formatting target value ranges
          // from the indicator definitions.
          var getTargetRanges = _.flow(
            _.property('bound_json'), // Extract bounds definition
            _.partial(_.reject, _, { bound_name: 'invalid' }), // Filter out the 'invalid' target ranges
            _.partial(_.map, _, _openBounds), // Replace 'NULL' with +/- Infinity
            _.partial(_.sortBy, _, _getBoundOrder) // Sort the bounds: bad, ok/okay, good
          )

          var bounds = _(columns)
            .indexBy('id')
            .mapValues(getTargetRanges)
            .omit(_.isEmpty)
            .value()

          var series = _.map(data[1].objects, function (d) {
            var dataIdx = _.indexBy(d.indicators, 'indicator')
            var name = d.location

            if (self.locations[name]) {
              name = self.locations[name]
            }

            if (name.name) {
              name = name.name
            }

            return {
              id: name,
              name: name,
              values: _.map(columns, function (indicator) {
                var v = {
                  id: name + '-' + indicator.id,
                  indicator: indicator.id
                }

                var id = indicator.id

                if (dataIdx[id]) {
                  v.value = dataIdx[id].value

                  if (util.defined(v.value)) {
                    _.each(bounds[id], function (bound) {
                      if (v.value >= bound.mn_val && v.value <= bound.mx_val) {
                        v.range = bound.bound_name
                      }
                    })
                  }
                }

                return v
              })
            }
          })

          self.columns = columns
          self.series = series
        }, this.error)
    },

    render: function () {
      var valueDefined = _.partial(util.defined, _, function (d) { return d.value })
      var notEmpty = _.partial(_.some, _, valueDefined)

      var visible = _(this.series)
        .pluck('values')
        .flatten()
        .groupBy('indicator')
        .mapValues(this.showEmpty ? _.constant(true) : notEmpty)
        .value()

      var props = {}

      props.headers = _.filter(
        this.columns,
        _.flow(_.property('id'), _.propertyOf(visible))
      )

      // Returns new series objects where the values property contains only
      // objects for indicators that are visible
      var filterInvisibleIndicators = function (s) {
        return _.assign({}, s, {
          values: _.filter(s.values, _.flow(_.property('indicator'), _.propertyOf(visible)))
        })
      }

      props.scale = d3.scale.ordinal()
          .domain(['bad', 'okay', 'ok', 'good'])
          .range(['#AF373E', '#959595', '#959595', '#2B8CBE'])

      props.cellSize = 36
      props.fontSize = 14
      props.onMouseOver = this.showTooltip
      props.onMouseOut = this.hideTooltip
      props.onClick = this.navigate
      props.onRowClick = this.navigate
      props.onColumnHeadOver = this.indicatorOver
      props.onColumnHeadOut = this.indicatorOut
      props.value = _.property('range')
      props.headerText = _.property('short_name')

      props.sortValue = function (series, col) {
        return (col === null)
          ? series.name
          : RANGE_ORDER[series.values[col].range]
      }

      var heatmap = React.createElement(Chart, {
        type: 'HeatMap',
        data: _.map(this.series, filterInvisibleIndicators),
        options: props
      })

      React.render(heatmap, this.$$.heatmap)
    },

    showTooltip: function (d) {
      var evt = d3.event
      var val = d.value
      var indicators = _.indexBy(this.columns, 'id')
      var histogram = d3.layout.histogram()
      var width = 120 * 1.618
      var height = 120

      var re = /(.+)-(\d+)/
      var match = re.exec(d.id)

      if (!match) {
        return
      }

      var data = _(this.series)
        .pluck('values')
        .flatten()
        .filter(function (d) { return d.indicator === Number(match[2]) })
        .pluck('value')

      var total_locations = data.size()

      data = data.reject(_.isNull)
        .thru(histogram)
        .value()

      // Don't show a tooltip for completely empty columns
      if (_.isEmpty(data) || _.all(data, function (d) { return d.y <= 0 })) {
        return
      }

      var xScale = d3.scale.linear()
        .domain([
          d3.min(data, _.property('x')),
          d3.max(data, function (d) {
            return d.x + d.dx
          })
        ])
        .range([0, width])

      var yScale = d3.scale.linear()
        .domain([0, d3.max(data, _.property('y'))])
        .range([height, 0])

      var scale = function (d) {
        var current = (val >= d.x) && (val <= (d.x + d.dx))

        return {
          width: xScale(d.x + d.dx) - xScale(d.x) - 1,
          height: height - yScale(d.y),
          x: xScale(d.x),
          y: yScale(d.y),
          bin: d.x,
          value: d.y,
          current: current
        }
      }

      var fmt = d3.format('%')

      var tick = function (t) {
        return {
          x: xScale(t),
          value: fmt(t)
        }
      }

      var targets = _(indicators[match[2]].bound_json)
        .reject(function (r) { return r.bound_name === 'invalid' })
        .sortBy(function (r) { return RANGE_ORDER[r.bound_name] })
        .map(function (r) {
          return {
            bound_name: r.bound_name,
            mn_val: fmt(r.mn_val),
            mx_val: fmt(r.mx_val)
          }
        })
        .value()

      this.$dispatch('tooltip-show', {
        el: this.$el,
        position: {
          x: evt.pageX,
          y: evt.pageY
        },
        data: {
          orientation: 'top',
          location: match[1],
          indicator: indicators[match[2]].short_name,
          total_locations: total_locations,
          reporting_locations: _.sum(data, 'y'),
          value: fmt(val),
          template: 'tooltip-heatmap',
          width: width,
          height: height,
          histogram: _(data)
            .filter(function (d) { return d.y > 0 })
            .map(scale)
            .value(),
          ticks: _(data)
            .pluck('x')
            .map(tick)
            .push({ x: width, value: fmt(xScale.domain()[1]) })
            .value(),
          targets: targets
        }
      })
    },

    hideTooltip: function () {
      this.$dispatch('tooltip-hide', {
        el: this.$el
      })
    },

    navigate: function (d) {
      var location = d

      if (!_.isString(d)) {
        var re = /(.+)-(\d+)/
        var match = re.exec(d.id)

        if (!match) {
          return
        }

        location = match[1]
      }

      this.$dispatch('tooltip-hide', {
        el: this.$el
      })

      page('/datapoints/management-dashboard/' + location + '/' +
        moment(this.campaign.start_date).format('YYYY/MM'))
    },

    indicatorOver: function (d, i, mouseover) {
      var indicators = _.indexBy(this.columns, 'short_name')

      this.$dispatch('tooltip-show', {
        el: this.$el,
        position: {
          x: d3.event.pageX,
          y: d3.event.pageY
        },
        data: {
          template: 'tooltip-indicator',
          name: d,
          orientation: 'top',
          description: indicators[d].description
        }
      })
    },

    indicatorOut: function () {
      this.$dispatch('tooltip-hide', { el: this.$el })
    }
  },

  watch: {
    'campaign': 'load',
    'columns': 'render',
    'location': 'load',
    'series': 'render',
    'showEmpty': 'render'
  }
}
