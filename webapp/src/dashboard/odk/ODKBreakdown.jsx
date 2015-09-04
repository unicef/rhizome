'use strict';

var _     = require('lodash');
var React = require('react');

var Chart      = require('component/Chart.jsx');
var DonutChart = require('component/DonutChart.jsx');
var Monitoring = require('dashboard/nco/Monitoring.jsx');

var ODKBreakdown = React.createClass({
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

    return <div>
      <div> <h1> this will be a breakdown </h1> </div>
    </div>
  }
});

module.exports = ODKBreakdown;
