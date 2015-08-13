var React = require('react/addons');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = Router;

var DocReviewApp = React.createClass({
	render: function() {
		return <div className="admin-container">
			<h1 className="admin-header">Document Review</h1>
			<ul className="admin-nav">
      <li><Link to="overview">Overview</Link></li>
      <li><Link to="mapping">Mapping</Link></li>
      <li><Link to="conflict">Dupes & Conflicts</Link></li>
      <li><Link to="validate">Validate</Link></li>
      <li><Link to="view_agg">View Aggregated</Link></li>
			</ul>
			<RouteHandler />
    </div>;

	}
});

var routes = (
      <Route name="app" path="/doc_review/" handler={DocReviewApp}>
          <Route name="overview" handler={require('./DocOverview')} />
					<Route name="mapping" handler={require('./DocMapping')} />
          <Route name="conflict" handler={require('./DocMapping')} />
          <Route name="validate" handler={require('./DocMapping')} />
          <Route name="view_agg" handler={require('./DocMapping')} />
      </Route>
);

module.exports = {
	render: function(container) {
		Router.run(routes, Router.HistoryLocation, Handler => {
			React.render(<Handler />, container)
		})
	}
};
