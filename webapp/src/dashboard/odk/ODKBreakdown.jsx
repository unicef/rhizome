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
        <div className='row'>
          <div className='small-6 columns'>
            <h3>VCM Summary</h3>
          </div>
          <div className='small-6 columns'>
            <h3>Health Camps</h3>
          </div>
      </div>
      <div className='row'>
        <div className='small-6 columns'>
          <h3>Birth Tracking</h3>
        </div>
        <div className='small-6 columns'>
          <h3>Supportive Supervision</h3>
        </div>
    </div>
    </div>
  }
});

module.exports = ODKBreakdown;
