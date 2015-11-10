'use strict'

var _ = require('lodash')
var d3 = require('d3')
var React = require('react')

var Chart = require('component/Chart.jsx')

var HeatMapTooltip = React.createClass({
  propTypes : {
    column    : React.PropTypes.string.isRequired,
    data      : React.PropTypes.array.isRequired,
    indicator : React.PropTypes.object.isRequired,
    row       : React.PropTypes.string.isRequired,
    value     : React.PropTypes.number.isRequired,
    total     : React.PropTypes.number.isRequired,

    format    : React.PropTypes.func
  },

  getDefaultProps : function () {
    return {
      format : d3.format('n')
    }
  },

  render : function () {
    var fmt = this.props.format
    var bounds = this.props.indicator.bound_json
    var value = this.props.value
    var targets

    if (!_.isEmpty(bounds)) {
      var rows = _(bounds)
        .reject(b => b.bound_name === 'invalid')
        .sortBy('mn_val')
        .map((b, i) => (
          <tr key={'bound-' + i}>
            <th>{b.bound_name}</th>
            <td className='numeric'>{fmt(b.mn_val)}</td>
            <td>&ndash;</td>
            <td>{fmt(b.mx_val)}</td>
          </tr>
        ))
        .value()

      targets = (
        <span>
          <h6>Targets</h6>
          <table className='indicator-ranges' style={{
              float  : 'left',
              margin : '0 1em 0 0'
            }}>
            {rows}
          </table>
        </span>
      )
    }

    var data = this.props.data
    var reported = _(data)
      .pluck('value')
      .filter(_.isFinite)
      .size()

    var chartOptions = {
      className  : d => _.inRange(value, d.x, d.x + d.dx) ? 'current' : null,
      yAxisTitle : 'Number of Districts',
      width      : 120 * 1.618,
      height     : 120,
      format     : fmt
    }

    return (
      <div>
        <h3>{this.props.row}</h3>
        <h4>{this.props.column}:&emsp;{fmt(value)}</h4>

        <h6>Distribution of Districts by Performance</h6>
        <Chart type='Histogram'
          data={data}
          options={chartOptions} />

        <div className='clearfix'></div>
        {targets}
        <p>
          {reported} / {this.props.total} locations reported values for {this.props.column}.
        </p>
      </div>
    )
  }
})

module.exports = HeatMapTooltip
