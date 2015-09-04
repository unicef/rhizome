'use strict';

var _     = require('lodash');
var React = require('react');

var Chart      = require('component/Chart.jsx');
var DonutChart = require('component/DonutChart.jsx');
var Monitoring = require('dashboard/nco/Monitoring.jsx');

var ODKMap = React.createClass({
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
    <div className='small-12 columns'>
      <h4 style={{ textAlign : 'center' }}> Non Compliance Map </h4>
    </div>



    </div>
  }
});

module.exports = ODKMap;
