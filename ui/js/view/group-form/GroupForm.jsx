'use strict';

var _      = require('lodash');
var React  = require('react');
var Reflux = require('reflux/src');

var GroupFormStore        = require("stores/GroupFormStore");
var GroupFormActions      = require('actions/GroupFormActions');
var IndicatorDropdownMenu = require('component/IndicatorDropdownMenu.jsx');
var List                  = require('component/list/List.jsx');

module.exports = React.createClass({

	mixins: [ Reflux.connect(GroupFormStore, 'store') ],

	submitForm: function(e) {
		GroupFormActions.saveGroupForm();
		e.preventDefault();
	},

	render: function() {

		var indicators = (<p>This role cannot enter data for any indicators.</p>);
		if (this.state.store.indicatorsSelected.length > 0) {
			indicators = (<div><p>This role can enter data for the following indicators:</p>
							  <List 
							  	items={this.state.store.indicatorsSelected} 
							  	removeItem={GroupFormActions.removeIndicatorSelection} />
						  </div>);
		}

		if (this.state.store.loading) {
			return (<div><i className="fa fa-spinner fa-spin"></i> Loading...</div>)
		}

		return (
			<form className="form inline user-account-container">

				<h2>Edit Role</h2>
				
				<div className="row">
					<div className="columns small-4 left-box">
						<h4>Role Name</h4>
					</div>
					<div className="columns small-8 right-box">
						<input id="role_name" type="text" value={this.state.store.groupName} />
					</div>
				</div>

				<div className="row">
					<div className="columns small-4 left-box">
						<h4>Indicator Permissions</h4>
					</div>
					<div className="columns small-8 right-box">
						<IndicatorDropdownMenu
							text='Add Indicators'
							icon='fa-plus'
							indicators={this.state.store.indicatorList}
							sendValue={GroupFormActions.addIndicatorSelection}>
						</IndicatorDropdownMenu>
						{indicators}
					</div>
				</div>

				<br /><br />

				<div className="row">
					<div className="columns small-4 left-box">
					</div>
					<div className="columns small-8 right-box">
						<button type="submit" className="btn btn-primary" onClick={this.submitForm}>Save Role</button>
					</div>
				</div>

			</form>
		);
	}
});