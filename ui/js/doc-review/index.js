var React = require('react/addons');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = Router;

var DocReviewApp = React.createClass({
	contextTypes: {
	router: React.PropTypes.func
	},

	render: function() {

	var q_params = this.context.router.getCurrentParams()
	console.log(q_params)

		// <Route name="doc_review" path="/doc_review/:docId" handler={DocReviewApp}/>

		return <div className="admin-container">
			<h1 className="admin-header">Document Review</h1>
			<ul className="admin-nav">
      <li><Link to="overview" params={q_params} >Overview</Link></li>
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
          <Route name="overview" path = "/doc_review/overview/:docId" handler={require('./DocOverview')} />
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
