var React = require('react/addons');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = Router;

var AdminApp = React.createClass({
	render: function() {
		return <div className="admin-container">
			<h1 className="admin-header">Admin Lists: </h1>
			<ul className="admin-nav">
				<li><Link to="users">Users</Link></li>
				<li><Link to="roles">Roles</Link></li>
				<li><Link to="regions">Regions</Link></li>
				<li><Link to="campaigns">Campaigns</Link></li>
				<li><Link to="indicators">Indicators</Link></li>
			</ul>
			<RouteHandler />
		</div>;
	}
});

var routes = (
	<Route name="app" path="/ufadmin/" handler={AdminApp}>
		<Route name="users" handler={require('./UsersAdmin')} />
		<Route name="roles" handler={require('./GroupsAdmin')} />
		<Route name="regions" handler={require('./RegionsAdmin')} />
		<Route name="campaigns" handler={require('./CampaignsAdmin')} />
		<Route name="indicators" handler={require('./IndicatorsAdmin')} />
	</Route>
);

module.exports = {
	render: function(container) {
		Router.run(routes, Router.HistoryLocation, Handler => {
			React.render(<Handler />, container)
		})
	}
};
