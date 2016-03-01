import _ from 'lodash'
import React from 'react'

import DashboardAPI from 'data/requests/DashboardAPI'

export default React.createClass({

  getInitialState () {
    return {
      customDashboards: []
    }
  },

  componentWillMount () {
    DashboardAPI.getDashboards().then(dashboards => {
      this.setState({customDashboards: dashboards})
    })
  },

  render () {
    let rows = <tr><td colSpan='3'>No custom dashboards created yet.</td></tr>

    if (_.isNull(this.state.customDashboards)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (this.state.customDashboards.length > 0) {
      rows = this.state.customDashboards.map(dashboard => {
        return (
          <tr>
            <td>
              <a href={'/dashboards/' + dashboard.id + '/'}>{dashboard.title} </a>
              <a href={'/dashboards/' + dashboard.id + '/edit/'}> edit</a>
            </td>
            <td>{dashboard.description}</td>
            <td>{dashboard.owner_username}</td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-12 columns'>
          <h5 className='all-dashboard'>all custom dashboard</h5>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Description</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
})
