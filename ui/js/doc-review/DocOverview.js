	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		propTypes : {
			doc_id 	: React.PropTypes.number.isRequired,
			loading : React.PropTypes.bool
		},

		getDefaultProps : function () {
			return {
				loading : false
			};
		},


		getInitialState : function () {
			return {
				doc_id       : null,
			};
		},

	  render() {

			var doc_id = this.props.doc_id
			var loading = this.props.loading

			console.log('logging doc id')
			console.log(doc_id)

			var refreshMasterUrl = '/source_data/refresh_master/' + doc_id
			var refreshMasterButton = refreshMasterUrl ?
				<div className="ufadmin-create-button">
					<a className="button" href={refreshMasterUrl}>Refresh Master</a>
				</div> : null;

			return <div>
			<h2> overview component doc ID : {doc_id} </h2>
			{refreshMasterButton}
		 </div>
		}
	});

	module.exports = DocOverview;
