'use strict';

var _ = require('lodash');
var React = require('react');

// var BarChartToggleSection = require('component/BarChartToggleSection.jsx');

var Breakdown = React.createClass({
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
    return (<h4>Coming Soon!</h4>);
  },

});

module.exports = Breakdown;
