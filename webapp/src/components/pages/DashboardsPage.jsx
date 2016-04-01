import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import DashboardStore from 'stores/DashboardStore'
import DashboardActions from 'actions/DashboardActions'

export default React.createClass({

  mixins: [
    Reflux.connect(DashboardStore, 'dashboards'),
  ],

  deleteDashboard (id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      DashboardActions.deleteDashboard(id)
    }
  },

  render () {
    const dashboards = this.state.dashboards.raw || []
    let rows = <tr><td colSpan='3'>No custom dashboards created yet.</td></tr>
    if (_.isNull(dashboards)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (dashboards.length > 0) {
      rows = dashboards.map(dashboard => {
        return (
          <tr>
            <td>
              <a href={'/dashboards/' + dashboard.id + '/'}>{dashboard.title} </a>
            </td>
            <td>
              <a onClick={() => this.deleteDashboard(dashboard.id) }>
                <i className='fa fa-trash'></i> Delete
              </a>
            </td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-3 columns'>&nbsp;</div>
        <div className='medium-6 columns'>
          <h5 className='all-dashboard'>All Dashboards</h5>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>&nbsp;</th>
              </tr>
            </thead>
            <tbody>
              {rows}
            </tbody>
          </table>
        </div>
        <div className='medium-3 columns'>&nbsp;</div>
      </div>
    )
  }
})
