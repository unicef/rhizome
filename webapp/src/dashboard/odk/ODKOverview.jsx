'use strict';

var _     = require('lodash');
var React = require('react');

var Chart      = require('component/Chart.jsx');
var DonutChart = require('component/DonutChart.jsx');
var Monitoring = require('dashboard/nco/Monitoring.jsx');

var Overview = React.createClass({
  propTypes : {
    data : React.PropTypes.object.isRequired,
    loading : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var loading    = this.props.loading;
    var data       = this.props.data;

    var options = {
      innerRadius : 0.6,
      domain      : _.constant([0, 1]),
      labelStyle  : {
        lineHeight : 1
      }
    };


    var caregiver_donut =
      <div className='medium-3 columns'>
        <DonutChart
        loading={loading}
        data={data.caregiverAwareness}
        options={options} />
      </div>
    return <div>
      <h1> HELLO </h1>
      <div>{caregiver_donut}</div>
    </div>
  }
});

module.exports = Overview;
