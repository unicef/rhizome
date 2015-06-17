'use strict';
var Reflux = require('reflux/src');
var _      = require('lodash');

var api = require('data/api');
var GroupFormActions = require('actions/GroupFormActions');

module.exports = Reflux.createStore({
	data: {
		groupId: 5,
		groupName: null,
		indicatorList: [],
		indicatorsSelected: [],
		loading: true
	},
	listenables: [ GroupFormActions ],
	getInitialState: function(){
		return this.data;
	},
	init: function(){
		var self = this;

		Promise.all([api.groups()])
			.then(_.spread(function(groups) {

				// find current group
				var g = _.find(groups.objects, function(d) { return d.id === self.data.groupId });
				self.data.groupName = g.name;
				console.log(self.data);

				self.data.loading = false;
				self.trigger(self.data);			
			}));

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
