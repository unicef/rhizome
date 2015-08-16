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
		API.admin.users({id:this.state.doc_overview.created_by_id}).then(function(result) {
			this.setState(uploaded_by_username: result.objects[0].username)
			}


    API.document({id:this.props.params.docId},null,{'cache-control':'no-cache'}).then(function(result) {
	      var api_data = result.objects[0];
	      if (this.isMounted()) {
	        this.setState({ doc_overview: api_data});
	      }
	    }.bind(this));
	  },

	  render() {
			var self = this;
			var uploaded_by_username =
				return result.objects[0].username
			}


			return <div>
			<h2> Document ID : {this.state.doc_overview.id} </h2>
			<h2> Document Name: {this.state.doc_overview.docfile} </h2>

			<h2> Uploaded By: {this.state.uploaded_by_username} </h2>

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
