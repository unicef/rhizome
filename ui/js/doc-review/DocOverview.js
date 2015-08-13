var React = require('react/addons');
var _ = require('lodash');
var API = require('../data/api');
var DropdownMenu     = require('component/DropdownMenu.jsx');

var DocOverview = React.createClass({
	render() {

		var overview = {
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
										// created at

										// searchable={true}
										// onSearch={this._setPattern}
										// {...props}>
										// {tag_tree}
										// sendValue={ChartBuilderActions.addIndicatorSelection}>


										}

		var indicators =  ['a','b','c']

		return <div>
		<h2> Document Name: {overview.doc_name} </h2>
		<h2> Uploaded By: {overview.created_by} </h2>
		<h2> Master Datapoint Count: {overview.master_datapoint_count} </h2>
		<h2> Source Datapoint Count: {overview.source_datapoint_count} </h2>
		<h2> Document to Source Datapoint: {overview.source_datapoint_time_elapsed} </h2>
		<h2> Latest Master Refresh: {overview.latest_refresh_master_time_elapsed} </h2>
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
