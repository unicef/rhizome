'use strict';

var _ = require('lodash');
var React = require('react');

var d3 = require('d3');

var HeatMapTooltip = React.createClass({
  propTypes : {
    column    : React.PropTypes.string.isRequired,
    data      : React.PropTypes.array.isRequired,
    indicator : React.PropTypes.object.isRequired,
    row       : React.PropTypes.string.isRequired,
    value     : React.PropTypes.number.isRequired,
    total     : React.PropTypes.number.isRequired,

    format    : React.PropTypes.func,
  },

  getDefaultProps : function () {
    return {
      format : d3.format('n'),
    };
  },

  render : function () {
    var fmt    = this.props.format;
    var bounds = this.props.indicator.bound_json;
    var targets;

    if (!_.isEmpty(bounds)) {
      var rows = _(bounds)
        .reject(b => b.bound_name === 'invalid')
        .map((b, i) => (
          <tr key={'bound-' + i}>
            <th>{b.bound_name}</th>
            <td className='numeric'>{fmt(b.mn_val)}</td>
            <td>&ndash;</td>
            <td>{fmt(b.mx_val)}</td>
          </tr>
        ))
        .value();

      targets = (
        <span>
          <h6>Targets</h6>
          <table className='indicator-ranges' style={{
              float  : 'left',
              margin : '0 1em 0 0'
            }}>
            {targets}
          </table>
        </span>
      );
    }

    var data = this.props.data;
    var reported = _(data)
      .pluck('value')
      .filter(_.isFinite)
      .size();

    return (
      <div>
        <h3>{this.props.row}</h3>
        <h4>{this.props.column}:&emsp;{fmt(this.props.value)}</h4>

        <h6>Distribution of Districts by Performance</h6>

        <div className='clearfix'></div>
        {targets}
        <p>
          {reported} / {this.props.total} regions reported values for {this.props.column}.
        </p>
      </div>
    );
  },
});

module.exports = HeatMapTooltip;
