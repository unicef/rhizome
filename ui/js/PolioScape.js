'use strict';

require('babel/polyfill');
var Vue = require('vue');
var React = require('react/addons');
window.React = React;

Vue.config.debug = true;

Vue.component('vue-dropdown', require('./component/dropdown'));
Vue.component('vue-table', require('./component/table'));
Vue.component('vue-table-editable', require('./component/table-editable'));
Vue.component('vue-pagination', require('./component/pagination'));
Vue.component('vue-tooltip', require('./component/tooltip'));
Vue.component('vue-menu', require('./component/menu'));

Vue.partial('tooltip-stacked-bar', require('./partial/tooltip-stacked-bar.html'));

var Component = { // React components
	UsersAdmin: require('./ufadmin/users.js')
};

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
	},
	UsersAdmin: function(el) {
		React.render(<Component.UsersAdmin />, document.getElementById('main'))
	}
};
