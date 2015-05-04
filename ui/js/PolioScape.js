'use strict';

var Vue = require('vue');

Vue.config.debug = true;

Vue.component('vue-dropdown', require('./component/dropdown'));
Vue.component('vue-table', require('./component/table'));
Vue.component('vue-table-editable', require('./component/table-editable'));
Vue.component('vue-pagination', require('./component/pagination'));
Vue.component('vue-tooltip', require('./component/tooltip'));
Vue.component('vue-menu', require('./component/menu'));

Vue.partial('tooltip-stacked-bar', require('./partial/tooltip-stacked-bar.html'));
Vue.partial('tooltip-heatmap', require('./partial/tooltip-heatmap.html'));

module.exports = {
	Explorer: function (el) {
		new Vue({
			el: el,
			components: { 'uf-explorer': require('./view/explorer') }
		});
	},
	Dashboard: function (el) {
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
