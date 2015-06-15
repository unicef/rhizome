'use strict';

var _      = require('lodash');
var React  = require('react');

var api = require('data/api');

var NavigationStore = require('stores/NavigationStore');

module.exports = React.createClass({

  getInitialState: function() {
    return {
      customDashboards: []
    };
  },

  componentWillMount : function () {
    this.customDashboards = NavigationStore.loadCustomDashboards();
  },

  render : function () {
    return (
      <h2>Test</h2>
    );
  }

});
