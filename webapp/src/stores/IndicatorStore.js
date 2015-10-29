'use strict';

var _      = require('lodash');
var Reflux = require('reflux');

var api = require('data/api');

var IndicatorStore = Reflux.createStore({

	listenables : [require('actions/AppActions')],

	init : function () {
		this.indicators = [];
	},

	getInitialState : function () {
		return {
			indicators : this.indicators
		};
	},

	onInit : function () {
		api.indicators(null, null, {'cache-control': 'no-cache'}).then(function (response) {
			var indicators = response.objects;

			this.indicators = _.indexBy(indicators, 'id');

			this.trigger({ indicators : indicators });
		}.bind(this));
	},

	getById : function (/* ids */) {
		return _(arguments)
			.map(function (id) {
				return this.indicators[id];
			}.bind(this))
			.filter()
			.value();
	},

});

module.exports = IndicatorStore;
