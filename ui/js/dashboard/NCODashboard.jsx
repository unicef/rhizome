'use strict';

var _ = require('lodash');
var React = require('react');

// var Overview = require('dashboard/nco/Overview.jsx');
// var Breakdown = require('dashboard/nco/Breakdown.jsx');

var NCODashboard = React.createClass({
  propTypes : {
    data      : React.PropTypes.oneOfType([
      React.PropTypes.array,
      React.PropTypes.object
    ]),
    dashboard : React.PropTypes.object.isRequired,

    loading   : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    return (<h1>Coming Soon!</h1>);
  }
});

module.exports = NCODashboard;
