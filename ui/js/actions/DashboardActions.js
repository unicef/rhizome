'use strict';

var Reflux = require('reflux/src');

var DashboardActions = Reflux.createActions([
	'setDashboard',
  'setRegion'
]);

module.exports = DashboardActions;
