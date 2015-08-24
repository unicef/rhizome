'use strict';

var Reflux = require('reflux/src');

var DashboardActions = Reflux.createActions([
	'setDashboard',
  'setRegion',
  'navigate'
]);

module.exports = DashboardActions;
