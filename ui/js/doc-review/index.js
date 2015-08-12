var React = require('react/addons');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = Router;

var DocReviewApp = React.createClass({
    render:function() {
        return(<div>
           <Router.RouteHandler/>
        </div>);
    }
});

var routes = (
      <Route name="app" path="/doc_review/" handler={DocReviewApp}>
					<Route name="doc_detail" handler={require('./DocDetail')} />
      </Route>
);

module.exports = {
	render: function(container) {
		Router.run(routes, Router.HistoryLocation, Handler => {
			React.render(<Handler />, container)
		})
	}
};
