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

Vue.filter('num', require('./filter/num'));

Vue.partial('tooltip-stacked-bar', require('./partial/tooltip-stacked-bar.html'));
Vue.partial('tooltip-heatmap', require('./partial/tooltip-heatmap.html'));
Vue.partial('tooltip-indicator', require('./partial/tooltip-indicator.html'));

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
	FieldMapping: function (el,document_id) {
		new Vue({
			el: el,
			components: { 'uf-field-mapping': require('./view/field-mapping') },
			data:{'document_id':document_id}/*,
			attached: function () {
			  Vue.component('field-mapping', require('./view/field-mapping'));
			  var FieldMapping = require('../../component/dropdown');
			  var fieldMapping = new FieldMapping({
			     		el : '#field-mapping-container'
			     	});
			}*/
		})
	},
	UsersAdmin: function(el) {
		React.render(<Component.UsersAdmin />, document.getElementById('main'));
	}
};
