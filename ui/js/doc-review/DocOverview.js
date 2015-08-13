	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		propTypes: {
			overview: React.PropTypes.string.isRequired,
		},

		getOverview: function() {
				var self = this;
				API.document({id:7}).then(function(data){
					this.props.overview = data.objects[0]
					return data.objects[0]
			});
		},

	  render() {
			var doc_overview = {
											'doc_name':'sample document name',
											'created_by':'john',
											'source_datapoint_count':101010,
											'source_datapoint_zero_count':244,
											'source_datapoint_null_count':8980,
											'master_datapoint_count':101,
											'campaign_col':'start_date',
											'region_code_col':'wardcode',
											'source_datapoint_time_elapsed': 72,
											'latest_refresh_master_time_elapsed': 7
											}


			return <div>
			<h2> Document Name: {doc_overview.doc_file} </h2>
			<h2> Uploaded By: {doc_overview.created_by} </h2>
			<h2> Master Datapoint Count: {doc_overview.master_datapoint_count} </h2>
			<h2> Source Datapoint Count: {doc_overview.source_datapoint_count} </h2>
			<h2> Document to Source Datapoint: {doc_overview.source_datapoint_time_elapsed} </h2>
			<h2> Latest Master Refresh: {doc_overview.latest_refresh_master_time_elapsed} </h2>
			<DropdownMenu
				text='Campaign Column'
				searchable={true}
				onSearch={this._setPattern}
			>
			</DropdownMenu>
			<DropdownMenu
				text='Region Column'
				searchable={true}
				onSearch={this._setPattern}
			>
			</DropdownMenu>
		 </div>
		}
	});

	module.exports = DocOverview;
