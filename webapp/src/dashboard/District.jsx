'use strict'

var _ = require('lodash')
var React = require('react')
var Layer = require('react-layer')
import d3 from 'd3'

var Chart = require('component/Chart.jsx')
var HeatMapTooltip = require('component/HeatMapTooltip.jsx')
var Tooltip = require('component/Tooltip.jsx')

var DashboardActions = require('actions/DashboardActions')

var formatUtil = require('util/format')
var legend = require('chart/renderer/legend')

var District = React.createClass({
  propTypes: {
    indicators: React.PropTypes.object,
    data: React.PropTypes.object,
    loading: React.PropTypes.bool
  },

  getInitialState: function () {
    return {
      showEmpty: false
    }
  },

  render: function () {
    // Hash of indicators that have bounds defined for easy filtering
    var indicators = _(this.props.indicators)
      .indexBy('id')
      .mapValues(ind => !_.isEmpty(ind.bound_json))
      .value()

    // List of indicator definitions based on the hash of indicator IDs who
    // have bounds defined
    var indicatorList = _.filter(this.props.indicators, ind => indicators[ind.id])

    // Map indicator IDs to a d3 threshold scale for determining into what
    // target range a value falls for a given indicator
    var targets = _(indicatorList)
      .indexBy('id')
      .mapValues(ind => {
        var bounds = _(ind.bound_json)
          .reject(b => b.bound_name === 'invalid')
          .map(b => [b.bound_name, _.isNumber(b.mn_val) ? b.mn_val : -Infinity])
          .sortBy('1')

        var extents = bounds.pluck('1').slice(1).value()
        var names = bounds.pluck('0').value()

        return d3.scale.threshold()
          .domain(extents)
          .range(names)
      })
      .value()

    // Scale for coloring based on pre-defined values
    var scale = d3.scale.ordinal()
      .domain(['bad', 'ok', 'good'])
      .range(['#DB5344', '#79909F', '#2FB0D3'])

    var lgnd = legend()
      .size(14)
      .scale(d3.scale.ordinal()
        .domain(['bad', 'ok', 'good'])
        .range(['#DB5344', '#79909F', '#2FB0D3'])
      )

    // Clean the data by first removing any data whose values are not finite -
    // i.e. undefined - or whose indicators have no target bounds defined, then
    // remove any series (rows) that have no data
    var data = _(this.props.data['district-heat-map'])
      .map(s => ({
        name: s.name,
        values: _.filter(s.values, d => indicators[d.indicator.id] && _.isFinite(d.value))
      }))
      .reject(s => _.isEmpty(s.values))
      .value()

    // Hash indicator IDs to a boolean indicating whether that column is
    // non-empty (true) or empty (false)
    var visible = _(data)
      .pluck('values')
      .flatten()
      .groupBy('indicator.id')
      .mapValues(v => _(v).pluck('value').some(_.isFinite))
      .value()

    // Determine what headers are shown based on whether or not the "Show empty
    // columns" checkbox is on
    var headers = this.state.showEmpty
      ? indicatorList
      : _.filter(indicatorList, i => visible[i.id])

    var options = {
      cellSize: 36,
      fontSize: 14,
      headers: headers,
      scale: d => scale(_.get(targets, d.indicator.id, _.noop)(d.value)),
      legend: lgnd,
      onMouseMove: this._onMouseMove,
      onMouseOut: this._onMouseOut,
      onColumnHeadOver: this._onHeaderOver,
      onColumnHeadOut: this._onHeaderOut,
      onClick: this._onlocationClick,
      onRowClick: this._onlocationClick
    }

    return (
      <div id='district-dashboard'>
        <div className='row'>
          <form className='small-12 columns'>
            <label>
              <input type='checkbox'
                     checked={this.state.showEmpty}
                     onChange={this._setShowEmpty}/>&ensp;
              Show empty columns
            </label>
          </form>
        </div>

        <div className='row'>
          <div className='small-12 columns'>
            <Chart type='HeatMapChart'
                   loading={this.props.loading}
                   data={data}
                   options={options}/>
          </div>
        </div>
      </div>
    )
  },

  componentWillUnmount: function () {
    if (this.tip) {
      this.tip.destroy()
    }

    if (this.timer) {
      window.clearTimeout(this.time)
    }
  },

  _setShowEmpty: function (evt) {
    this.setState({ showEmpty: evt.target.checked })
  },

  _onMouseMove: function (d) {
    if (this.timer) {
      window.clearTimeout(this.timer)
      this.timer = null
    }

    var column = d.indicator.short_name
    var data = _(this.props.data['district-heat-map'])
      .pluck('values')
      .flatten()
      .filter(datum => datum.indicator.short_name === column)
      .clone()

    var evt = d3.event
    var total = _(this.props.data['district-heat-map'])
      .map(s => ({
        name: s.name,
        values: _.filter(s.values, d => _.isFinite(d.value))
      }))
      .reject(s => _.isEmpty(s.values))
      .size()

    var render = function () {
      var tip = React.createElement(HeatMapTooltip, {
        column,
        data,
        total,
        format: formatUtil.general,
        indicator: d.indicator,
        row: d.location.name,
        value: d.value
      })

      return React.createElement(Tooltip, {
        left: evt.pageX,
        top: evt.pageY
      }, tip)
    }

    if (!this.tip) {
      this.tip = new Layer(document.body, render)
    } else {
      this.tip._render = render
    }

    this.tip.render()
  },

  _onMouseOut: function (d) {
    if (this.tip && !this.timer) {
      var self = this

      this.timer = window.setTimeout(function () {
        self.tip.destroy()
        self.tip = null
        self.timer = null
      }, 200)
    }
  },

  _onHeaderOver: function (d) {
    var indicator = _.find(this.props.indicators, ind => ind.short_name === d)

    if (this.timer) {
      window.clearTimeout(this.timer)
      this.timer = null
    }

    var evt = d3.event

    var render = function () {
      return (
        <Tooltip left={evt.pageX} top={evt.pageY}>
          <div>
            <h3>{indicator.name}</h3>

            <p>{indicator.description}</p>
          </div>
        </Tooltip>
      )
    }

    if (!this.tip) {
      this.tip = new Layer(document.body, render)
    } else {
      this.tip._render = render
    }

    this.tip.render()
  },

  _onHeaderOut: function () {
    if (this.tip) {
      this.tip.destroy()
      this.tip = null
    }

    if (this.timer) {
      window.clearTimeout(this.timer)
      this.timer = null
    }
  },

  _onlocationClick: function (d) {
    var params = {
      dashboard: 'management-dashboard',
      location: _.isString(d) ? d : d.location.name
    }

    DashboardActions.navigate(params)
  }
})

module.exports = District
