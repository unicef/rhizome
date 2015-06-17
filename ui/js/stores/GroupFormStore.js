'use strict';
var Reflux = require('reflux/src');
var _      = require('lodash');

var api = require('data/api');
var GroupFormActions = require('actions/GroupFormActions');

module.exports = Reflux.createStore({
	data: {
		indicatorList: [],
		indicatorsSelected: [],
		loading: false
	},
	listenables: [ GroupFormActions ],
	getInitialState: function(){
		return this.data;
	},
	init: function(){
		var self = this;

		// api.groups.then(function(groups) {
			
		// });

		api.indicatorsTree().then(function(items) {
			self._indicatorIndex = _.indexBy(items.flat, 'id');
			self.data.indicatorList = _(items.objects)
				.sortBy('title')
				.value();
			self.trigger(self.data);
		});

	},
	onAddIndicatorSelection: function(value) {
		this.data.indicatorsSelected.push(this._indicatorIndex[value]);
	    this.trigger(this.data);
	},
	onRemoveIndicatorSelection: function(id) {
		_.remove(this.data.indicatorsSelected, {id:id});
		this.trigger(this.data);
	}
});
