var React = require('react/addons');
var _ = require('lodash');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = Router;

//var Page = {
//	Users: require('./users')
//};

var AdminApp = React.createClass({
	render: function() {
		return <div>
			<h1>Admin Entity Lists</h1>
			<ul>
				<li><Link to="users">Users</Link></li>
				<li><Link to="groups">Groups</Link></li>
				<li><Link to="regions">Regions</Link></li>
				<li><Link to="campaigns">Campaigns</Link></li>
				<li><Link to="indicators">Indicators</Link></li>

			</ul>
			<RouteHandler />
		</div>;
	}
});


var Page = {
	UserAdmin: require('./users'),
	GroupAdmin: React.createClass({
		render: function() { return <div>GroupAdmin</div>; }
	}),
	RegionAdmin: React.createClass({
		render: function() { return <div>RegionAdmin</div>; }
	}),
	CampaignAdmin: React.createClass({
		render: function() { return <div>CampaignAdmin</div>; }
	}),
	IndicatorAdmin: React.createClass({
		render: function() { return <div>IndicatorAdmin</div>; }
	})
};


var routes = (
	<Route name="app" path="/ufadmin/" handler={AdminApp}>
		<Route name="users" handler={Page.UserAdmin} />
		<Route name="groups" handler={Page.GroupAdmin} />
		<Route name="regions" handler={Page.RegionAdmin} />
		<Route name="campaigns" handler={Page.CampaignAdmin} />
		<Route name="indicators" handler={Page.IndicatorAdmin} />
	</Route>
);

module.exports = {
	render: function(container) {
		Router.run(routes, Router.HistoryLocation, Handler => {
			React.render(<Handler />, container)
		})
	}
};
