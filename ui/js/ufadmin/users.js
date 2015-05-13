'use strict';

var React = require('react/addons');
var _ = require('lodash');
var http = require('superagent');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SimpleDataTableColumn,
	SearchBar,
	FilterPanel, FilterInputCheckbox
} = require('react-datascope');

var API = require('../data/api');

var UsersAdmin = React.createClass({
	getInitialState: function() {
		return {
			query: {}
		};
	},
	componentDidMount: function() {
		API.admin.usersMetadata().done(response => {
			// todo handle error
			//console.log(response.body);
			//this.setState({metadata: response.body});
			this.setState({metadata: response.objects});
		});
		API.admin.users().done(response => {
			//var {meta, objects} = response.body;
			//var {limit, offset, total_count} = meta;
			//this.setState({users: objects, limit, offset, count: total_count});

			//var users = response.body;
			this.setState({users: response.objects});
		});
	},
	onChangeQuery: function(query) {
		this.setState({query});
	},

	render: function() {
		var searchableFieldNames = this.state.metadata ?
			_(this.state.metadata.fields).filter(f => f.searchable).pluck('name').value() : [];
		console.log(this.state);
		return (
			<div>
				<h1>Users Admin Page</h1>

				{_.isArray(this.state.users) && this.state.metadata ?
					<LocalDatascope
						data={this.state.users}
						schema={{fields: this.state.metadata.fields}}
						>
						<Datascope>

							<SearchBar
								id="search-all"
								fields={searchableFieldNames}
								placeholder="Search users"
							/>

							<SimpleDataTable>
								<SimpleDataTableColumn name="first_name"/>
								<SimpleDataTableColumn name="last_name"/>
								<SimpleDataTableColumn name="email"/>
							</SimpleDataTable>

						</Datascope>
					</LocalDatascope>
				: "loading..."}
			</div>
		)
	}
});


module.exports = UsersAdmin;
