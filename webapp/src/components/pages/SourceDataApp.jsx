import React from 'react'
import Router from 'react-router'

var {Route, RouteHandler, Link} = Router
var SourceDataApp = React.createClass({
  contextTypes: {
    router: React.PropTypes.func
  },

  render: function () {
    // var q_params = this.context.router.getCurrentParams()

    return <div className='admin-container'>
      <ul className='admin-nav'>
        <li><Link to='users'>Users</Link></li>
      </ul>
      <RouteHandler/>
    </div>
  }
})

var routes = (
    <Route name='app' path='/source-data/' handler={SourceDataApp}>
      <Route name='users' handler={require('components/organisms/manage-system/UsersAdmin')} />
  </Route>
)

export default {
  render: function (container) {
    Router.run(routes, Router.HistoryLocation, Handler => {
      React.render(<Handler />, container)
    })
  }
}
