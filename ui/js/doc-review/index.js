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
	};

	console.log(q_params)

		return <div className="admin-container">
			<h1 className="admin-header">Document Review</h1>
			<ul className="admin-nav">
      <li><Link to="overview" params={q_params} >Overview</Link></li>
			<li><Link to="mapping" params={q_params}>Mapping</Link></li>
      <li><Link to="conflict" params={q_params}>Dupes & Conflicts</Link></li>
      <li><Link to="validate" params={q_params}>Validate</Link></li>
      <li><Link to="view_agg" params={q_params}>View Aggregated</Link></li>
      <li><Link to="doc_index" >Document Index</Link></li>
			</ul>
			<RouteHandler />
    </div>;
	}
});

var routes = (
      <Route name="app" path="/doc_review/" handler={DocReviewApp}>
          <Route name="overview" path = "overview/:docId" handler={require('./DocOverview')} />
          <Route name="mapping" path = "mapping/:docId" handler={require('./DocMapping')} />
					<Route name="conflict" path = "conflict/:docId" handler={require('./DocMapping')} />
					<Route name="validate" path = "validate/:docId" handler={require('./DocMapping')} />
					<Route name="view_agg" path = "view_agg/:docId" handler={require('./DocMapping')} />
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
