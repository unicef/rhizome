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

		Promise.all([ 
				api.indicatorsTree(), 
				api.groups(), 
				api.group_permissions({ group: self.data.groupId }) 
			])
			.then(_.spread(function(indicators, groups, groupPermissions) {

				// find current group
				var g = _.find(groups.objects, function(d) { return d.id === self.data.groupId });
				self.data.groupName = g.name;

				// process indicators
				self._indicatorIndex = _.indexBy(indicators.flat, 'id');
				self.data.indicatorList = _(indicators.objects)
					.sortBy('title')
					.value();

				// select current permissions
				_.each(groupPermissions.objects, function(d) {
					if (d.indicator_id) {
						self.data.indicatorsSelected.push(self._indicatorIndex[d.indicator_id]);
					}
				});

				self.data.loading = false;
				self.trigger(self.data);			
			}));

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
