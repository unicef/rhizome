	var React = require('react/addons');
	var _ = require('lodash');
	var API = require('../data/api');
	var DropdownMenu     = require('component/DropdownMenu.jsx');

	var DocOverview = React.createClass({
		// propTypes: {
		// 	overview: React.PropTypes.string//.isRequired,
		// },
		getInitialState: function() {
				// https://facebook.github.io/react/tips/initial-ajax.html
				return {
		      doc_overview: {'docfile':'someTest'}
		    };
		},

		componentDidMount: function() {
    API.document({id:7}).then(function(result) {
	      var api_data = result.objects[0];
	      if (this.isMounted()) {
	        this.setState({
	          doc_overview: api_data,
	        });
	      }
	    }.bind(this));
	  },

	  render() {
			var self = this;
			return <div>
			<h2> Document Name: {this.state.doc_overview.docfile} </h2>
		 </div>
		}
	});

	module.exports = DocOverview;
