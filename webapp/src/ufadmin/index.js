import React from 'react'
import Router from 'react-router'
var {Route, RouteHandler, Link} = Router
import SimpleForm from './SimpleForm'

var AdminApp = React.createClass({
  contextTypes: {
    router: React.PropTypes.func
  },

  render: function () {
    var q_params = this.context.router.getCurrentParams()

    return <div className='admin-container'>
      <ul className='admin-nav'>
        <li><Link to='manage' params={{'id': q_params['id'], 'contentType': 'indicator'}} >Manage Indicators</Link></li>
        <li><Link to='manage' params={{'id': q_params['id'], 'contentType': 'indicator_tag'}} >Manage Tags</Link></li>
        <li><Link to='users'>Users</Link></li>
        <li><Link to='locations'>locations</Link></li>
        <li><Link to='campaigns'>Campaigns</Link></li>
        <li><Link to='indicators'>Indicators</Link></li>
        <li><Link to='tags'>Tags</Link></li>
      </ul>
      <RouteHandler/>
    </div>
  }
})

var routes = (
    <Route name='app' path='/manage_system/' handler={AdminApp}>
      <Route name='manage' path='/manage_system/manage/:contentType/:id?' handler={SimpleForm}/>
      <Route name='users' handler={require('./UsersAdmin')} />
      <Route name='locations' handler={require('./RegionAdmin')} />
      <Route name='campaigns' handler={require('./CampaignsAdmin')} />
      <Route name='indicators' handler={require('./IndicatorsAdmin')} />
      <Route name='tags' handler={require('./TagsAdmin')} />
  </Route>
)

export default {
  render: function (container) {
    Router.run(routes, Router.HistoryLocation, Handler => {
      React.render(<Handler />, container)
    })
  }
}
