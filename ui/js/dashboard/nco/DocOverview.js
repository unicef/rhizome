	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		// propTypes : {
		// 	indicators    : React.PropTypes.object.isRequired,
		// 	region    : React.PropTypes.object.isRequired,
		// 	loading   : React.PropTypes.bool
		// },

		getDefaultProps : function () {
			return {
				loading : false
			};
		},

		getInitialState: function() {
				// https://facebook.github.io/react/tips/initial-ajax.html
				return {doc_overview: {'docfile':null}, indicators: {'indicators':null}};
		},


		componentDidMount: function() {

    API.document({id:this.props.params.docId},null,{'cache-control':'no-cache'}).then(function(result) {
	      var api_data = result.objects[0];
	      if (this.isMounted()) {
	        this.setState({doc_overview:api_data});
	      }
	    }.bind(this));
		},


	  render() {
			var self = this;

			var refreshMasterUrl = '/source_data/refresh_master/' + this.props.params.docId
			var refreshMasterButton = refreshMasterUrl ?
				<div className="ufadmin-create-button">
					<a className="button" href={refreshMasterUrl}>Refresh Master</a>
				</div> : null;

			return <div>
			<h2> Document ID : {this.state.doc_overview.id} </h2>
			<h2> Document Name: {this.state.doc_overview.docfile} </h2>

			<h2> Uploaded By: {this.state.doc_overview.created_by_id} </h2>
			{refreshMasterButton}


		 </div>
		}
	});

	module.exports = DocOverview;
