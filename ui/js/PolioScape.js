'use strict';

var Vue = require('vue');
var page = require('page');

Vue.config.debug = true;

Vue.component('vue-dropdown', require('./component/dropdown'));
Vue.component('vue-table', require('./component/table'));
Vue.component('vue-pagination', require('./component/pagination'));

var app = new Vue({
	el: '#main',
	components: {
		'uf-dashboard': require('./view/dashboard'),
		'uf-explorer': require('./view/explorer')
	},
	data: {
		currentView: 'uf-dashboard'
	}
});

function setView(view) {
	return function () {
		app.$data.currentView = view;
	};
}

page('/', setView('uf-dashboard'));
page('/data', setView('uf-explorer'));
page();
