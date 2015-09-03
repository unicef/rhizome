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
				docfile: null,
				doc_title: null,
				doc_datapoint_cnt: null,
				source_submission_total_cnt: null,
				source_submission_to_process_cnt: null,

			};
		},

		componentWillMount : function (nextProps, nextState) {
					this.pullDocDetails()
			},

		componentWillUpdate : function (nextProps, nextState) {
				if (nextProps.doc_id != this.props.doc_id) {
					return;
				}
			},

		pullDocDetails : function () {

			api.docDetail({document_id: this.props.doc_id},null,{'cache-control':'no-cache'})
			.then(response => this.setState({
				doc_deets: response.objects,
			}));
		},

		refreshMaster : function () {

				api.refresh_master({document_id: this.props.doc_id},null,{'cache-control':'no-cache'})
				.then(response => this.setState({
					docfile: response.objects[0].docfile,
					doc_title: response.objects[0].doc_title,
					doc_datapoint_cnt: response.objects[0].doc_datapoint_cnt,
					source_submission_total_cnt: response.objects[0].source_submission_total_cnt,
					source_submission_to_process_cnt: response.objects[0].source_submission_to_process_cnt,
				}));
			},

		renderLoading() {
			return <div className='admin-loading'> Doc Details Loading...</div>
		},

	  render() {
			var doc_id = this.props.doc_id;
			var doc_tab = this.props.doc_tab;
			var doc_deets = this.state.doc_deets;

			if(!doc_deets) return this.renderLoading();

		  var refresh_master_btn = <div>
				<button className="tiny" onClick={this.refreshMaster}> Refresh Master!
				</button>
				</div>

			var doc_detail_list = []

			var rows = [];
			for (var i=0; i < doc_deets.length; i++) {
			    // rows.push(<ObjectRow />);
					var doc_detail = doc_deets[i]
					console.log(doc_detail.doc_detail_type_id)
					rows.push(<li>{doc_detail.doc_detail_type} : {doc_detail.doc_detail_value} </li>)
					// rows.push(<li> doc_detail['doc_detail_type_id'] : doc_detail['doc_detail_value'] </li>);
			}

			return <div>

			<h3> Document Overview </h3>
			<ul>{rows}</ul>

			{refresh_master_btn}
		 </div>
		}
	});

	module.exports = DocOverview;
