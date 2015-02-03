'use strict';

var Vue = require('vue');
var log = require('./util/log');

log.level = log.DBG;


Vue.config.debug = true;

Vue.component('vue-dropdown', require('./component/dropdown'));
Vue.component('vue-table', require('./component/table'));
Vue.component('vue-table-editable', require('./component/table-editable'));
Vue.component('vue-pagination', require('./component/pagination'));
Vue.component('vue-tooltip', require('./component/tooltip'));

module.exports = {
	Explorer: function (el) {
		new Vue({
			el: el,
			components: { 'uf-explorer': require('./view/explorer') }
		});
	},
	Dashboard: function (el) {
		log.info('Dashboard', 'init');

		new Vue({
			el: el,
			components: { 'uf-dashboard': require('./view/dashboard') }
		});
	},
	DataEntry: function (el) {
		new Vue({
			el: el,
			components: { 'uf-entry-form': require('./view/entry-form') }
		});
	}
};
