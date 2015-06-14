'use strict';

var _ = require('lodash');
var React = require('react');

var Chart = require('component/Chart.jsx');

var DonutChart = React.createClass({
  propTypes : {
    data    : React.PropTypes.array.isRequired,
    options : React.PropTypes.object,
    label   : React.PropTypes.func
  },

  getDefaultProps : function () {
    return {
      label : _.noop
    };
  },

  render : function () {
    var labelText = this.props.label(this.props.data);
    var label;

    if (!_.isEmpty(labelText)) {
      label = (<p className='donut-label'>{labelText}</p>);
    }

    return (
      <div className='labeled-donut'>
        <Chart type='PieChart' data={this.props.data} options={this.props.options} />
        {label}
      </div>
    );
  },
});

module.exports = DonutChart;
