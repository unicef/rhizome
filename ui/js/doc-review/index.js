var React = require('react/addons');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler,NotFoundRoute, NotFound, Redirect, Link} = Router;

var DocReviewApp = React.createClass({
	contextTypes: {
	router: React.PropTypes.func
	},

	render: function() {

	var q_params = this.context.router.getCurrentParams()

	if (!("docId" in q_params)){
		q_params['docId'] = 0

		return <div className="admin-container">
			<h1 className="admin-header">Document Review</h1>
			<ul className="admin-nav">
			<li><Link to="doc_index" params={q_params} >Document Index</Link></li>
			</ul>
			<RouteHandler />
		</div>;

	};

		return <div className="admin-container">
			</div>;
	}
});

var routes = (
      <Route name="app" path="/doc_review/" handler={DocReviewApp}>
					<Route name="doc_index" path = "doc_index/" handler={require('./DocIndex')} />
		</Route>
);

module.exports = {
	render: function(container) {
		Router.run(routes, Router.HistoryLocation, Handler => {
			React.render(<Handler />, container)
		})
	}
};
