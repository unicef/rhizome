var React = require('react/addons');
	var _ = require('lodash');
	var API = require('data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');
	var NavigationStore     = require('stores/NavigationStore');

	var DocOverview = React.createClass({
		propTypes : {
			doc_id 	: React.PropTypes.number.isRequired,
			doc_tab : React.PropTypes.string.isRequired,
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

		componentWillUpdate : function (nextProps, nextState) {
				if (nextProps.doc_id != this.props.doc_id) {
					console.log('updating')
					return;
				}
			},


	  render() {
			var doc_id = this.props.doc_id
			var doc_tab = this.props.doc_tab
			var loading = this.props.loading

			var refreshMasterUrl = '/source_data/refresh_master/' + doc_id
			var refreshMasterButton = refreshMasterUrl ?
				<div className="ufadmin-create-button">
					<a className="button" href={refreshMasterUrl}>Refresh Master</a>
				</div> : null;

			return <div>
			<h2> Document Overview </h2>
			<h3> doc_id : {doc_id} </h3>
			<div>{refreshMasterButton} </div>
		 </div>
		}
	});

	module.exports = DocOverview;
