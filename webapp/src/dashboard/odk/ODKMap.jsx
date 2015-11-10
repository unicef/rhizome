'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')

var Chart = require('component/Chart.jsx')
var DonutChart = require('component/DonutChart.jsx')
var Monitoring = require('dashboard/nco/Monitoring.jsx')

var ODKMap = React.createClass({
  propTypes : {
    data : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    }
  },

  render : function () {
    var loading = this.props.loading
    var data = this.props.data

    var missedChildrenMap = data.nonCompliance

    return <div className='row'>
        <h4> Missed Children</h4>
        <Chart type='ChoroplethMap'
          data={missedChildrenMap}
          loading={loading}
          options={{
            domain  : _.constant([0, 0.1]),
            value   : _.property('properties[475]'),
            yFormat : d3.format('%')
          }} />
        </div>
  }
})

module.exports = ODKMap
