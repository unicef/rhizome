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

function parseSchema(response) {
	//return response.objects;
	var schema = {
		$schema: "http://json-schema.org/draft-04/schema#",
		title: "Users",
		type: "array",
		items: {
			title: "User",
			type: "object",
			properties: _(response.objects.fields).map(field => {
				return [field.name, _.transform(field, (result, val, key) => {
					if(key === 'type' && val === 'datetime') {
						result.type = 'string';
						result.format = 'date-time';
					} else if(key === 'constraints') {
						if(val && val.items && val.items.oneOf && val.items.oneOf.length) {
							result.items = {type: typeof val, enum: val.items.oneOf};
						}
					} else if(_.includes(['type', 'title'], key)) {
						result[key] = val;
					}
				})]
			}).object().value()
		}
	};
	return schema;
}

var UsersAdmin = React.createClass({
	getInitialState: function() {
		return {
			query: {}
		};
	},
	componentDidMount: function() {
		API.admin.usersMetadata().done(response => {
			var schema = parseSchema(response);
			console.log('schema', schema);
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

		//<SearchBar
		//	id="search-all"
		//	fields={searchableFieldNames}
		//	placeholder="Search users"
		//	/>

		return (
			<div>
				<h1>Users Admin Page</h1>

				{_.isArray(this.state.users) && this.state.metadata ?
					<LocalDatascope
						data={this.state.users}
						schema={{fields: this.state.metadata.fields}}
						>
						<Datascope>
							<SimpleDataTable>
							</SimpleDataTable>
						</Datascope>
					</LocalDatascope>
				: "loading..."}
			</div>
		)
	}
});


module.exports = UsersAdmin;
