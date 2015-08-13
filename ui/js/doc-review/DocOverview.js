	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		getInitialState: function() {
				// https://facebook.github.io/react/tips/initial-ajax.html
				return { doc_overview: {'docfile':null}};
		},

		componentDidMount: function() {
    API.document({id:6}).then(function(result) {
	      var api_data = result.objects[0];
	      if (this.isMounted()) {
	        this.setState({ doc_overview: api_data});
	      }
	    }.bind(this));
	  },

	  render() {
			var self = this;
			return <div>
			<h2> Document Name: {this.state.doc_overview.docfile} </h2>
			<h2> Uploaded By: {this.state.doc_overview.created_by_id} </h2>
			<h2> Master Datapoint Count: {this.state.doc_overview.master_datapoint_count} </h2>
			<h2> Source Datapoint Count: {this.state.doc_overview.source_datapoint_count} </h2>
			<h2> Document to Source Datapoint: {this.state.doc_overview.source_datapoint_time_elapsed} </h2>
			<h2> Latest Master Refresh: {this.state.doc_overview.latest_refresh_master_time_elapsed} </h2>

			<DropdownMenu
				text='Campaign Column'
				searchable={true}
				// onSearch={this._setPattern}
			>
			</DropdownMenu>
			<DropdownMenu
				text='Region Column'
				searchable={true}
				// onSearch={this._setPattern}
			>
			</DropdownMenu>
		 </div>
		}
	});

	module.exports = DocOverview;
