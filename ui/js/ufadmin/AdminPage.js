var _ = require('lodash');

var React = require('react/addons');
var parseSchema = require('./utils/parseSchema');

var AdminPage = React.createClass({
	propTypes: {
		title: React.PropTypes.string.isRequired,
		getMetadata: React.PropTypes.func.isRequired,
		getData: React.PropTypes.func.isRequired
	},
	getInitialState: function() {
		return {
			data: null,
			schema: null,
			query: {}
		}
	},

	componentWillMount: function() {
		this.props.getMetadata().done(response => this.setState({schema: parseSchema(response)}));
		this.props.getData().done(response => this.setState({data: response.objects}));
	},

	render() {
		var isLoaded = _.isArray(this.state.data) && this.state.schema;
		if(!isLoaded) return this.renderLoading();

		var {data, schema} = this.state;
		return <div>
			<h2>{this.props.title} Admin Page</h2>

			{React.Children.map(this.props.children, child => {
				var childProps = {data, schema};
				return React.cloneElement(child, childProps);
			})}
		</div>
	},
	renderLoading() {
		return <div className='admin-loading'>Loading...</div>
	}
});


module.exports = AdminPage;
