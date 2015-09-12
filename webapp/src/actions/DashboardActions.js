'use strict';

var Reflux = require('reflux');

var DashboardActions = Reflux.createActions([
  'setDashboard',
  'setRegion',
  'navigate'
]);

module.exports = DashboardActions;
