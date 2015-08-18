'use strict';

var _     = require('lodash');
var React = require('react');

var Overview  = require('dashboard/nco/Overview.jsx');
var Breakdown = require('dashboard/nco/Breakdown.jsx');

var SourceDataDashboard = React.createClass({
  propTypes : {
    dashboard : React.PropTypes.object.isRequired,
    data      : React.PropTypes.object.isRequired,
    region    : React.PropTypes.object.isRequired,

    loading   : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var data    = this.props.data;
    var loading = this.props.loading;

    return (<h1> hi this is the document dashboard </h1>
    );
  }
});

module.exports = SourceDataDashboard;
