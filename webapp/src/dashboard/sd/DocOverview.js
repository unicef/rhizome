var React = require('react');
	var _ = require('lodash');
	var api = require('data/api');
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

		refreshMaster : function () {
				console.log('refreshing master')

				api.refresh_master({document_id: this.props.doc_id},null,{'cache-control':'no-cache'})
				.then(response => this.setState({
						some_var: 'hello'
						// source_object_code: response.objects[0].source_object_code,
						// content_type: response.objects[0].content_type,
				}));
			},

	  render() {
			var doc_id = this.props.doc_id;
			var doc_tab = this.props.doc_tab;
			var loading = this.props.loading;

		  var refresh_master_btn = <div>
				<button className="tiny" onClick={this.refreshMaster}> Refresh Master!
				</button>
				</div>

			return <div>
			<h2> Document Overview </h2>
			<h3> doc_id : {doc_id} </h3>
			{refresh_master_btn}
		 </div>
		}
	});

	module.exports = DocOverview;
