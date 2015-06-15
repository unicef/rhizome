'use strict';

var _      = require('lodash');
var React  = require('react');

var api = require('data/api');

var NavigationStore = require('stores/NavigationStore');

module.exports = React.createClass({

  render : function () {
    console.log(NavigationStore.dashboards);
    console.log(NavigationStore.customDashboards);
    return (
      <h2>Test</h2>
    );
  }

});
