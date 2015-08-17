	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		getInitialState: function() {
				// https://facebook.github.io/react/tips/initial-ajax.html
				return {doc_overview: {'docfile':null}};
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

			var createUrl = '/source_data/refresh_master/' + this.props.params.docId
			var createButton = createUrl ?
				<div className="ufadmin-create-button">
					<a className="button" href={createUrl}>Refresh Master</a>
				</div> : null;

			return <div>
			<h2> Document ID : {this.state.doc_overview.id} </h2>
			<h2> Document Name: {this.state.doc_overview.docfile} </h2>

			<h2> Uploaded By: {this.state.doc_overview.created_by_id} </h2>
			{createButton}


		 </div>
		}
	});

	module.exports = DocOverview;
