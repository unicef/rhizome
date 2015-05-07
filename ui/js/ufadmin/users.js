//'use strict';

var React = require('react/addons');
var _ = require('lodash');
var http = require('superagent');

var {
	Datascope, LocalDatascope,
	SimpleDataTable, SearchBar,
	FilterPanel, FilterInputCheckbox
} = require('react-datascope');

var API = {
	// spec: https://seedscientific.atlassian.net/wiki/display/CE/Site+Admin+API+Specs
	getMetadata: function() {
		return http.get('/api/v1/entity/users/metadata/');
	},
	getUsers: function(query) {
		// allowed query params:
		// limit, offset, search, filter, sort, sort_direction
		return http.get('/api/v1/entity/users/').query(query);
	}
};


var UsersAdmin = React.createClass({
	getInitialState: function() {
		return {
			query: {}
		};
	},
	componentDidMount: function() {
		API.getMetadata().end((err, response) => {
			// todo handle error
			this.setState({metadata: response.body});
		});
		API.getUsers().end((err, response) => {
			console.log(response);
			var {meta, objects} = response.body;
			var {limit, offset, total_count} = meta;
			this.setState({users: objects, limit, offset, count: total_count});
		});
	},
	onChangeQuery: function(query) {
		this.setState({query});
	},

	render: function() {
		var searchableFieldNames = this.state.metadata ?
			_(this.state.metadata.fields).filter(f => f.searchable).pluck('name').value() : [];
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

							<FilterPanel>
								<FilterInputCheckbox field='groups' />
							</FilterPanel>

							<SimpleDataTable />

						</Datascope>
					</LocalDatascope>
				: "loading..."}
			</div>
		)
	}
});


module.exports = UsersAdmin;
