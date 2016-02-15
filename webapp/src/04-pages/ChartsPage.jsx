import _ from 'lodash'
import React from 'react'

import ChartAPI from 'data/requests/ChartAPI'

var ChartsPage = React.createClass({

  getInitialState () {
    return {
      customCharts: []
    }
  },

  componentWillMount () {
    ChartAPI.getCharts().then(charts => {
      this.setState({customCharts: charts})
    })
  },

  render () {
    let rows = <tr><td colSpan='3'>No custom charts created yet.</td></tr>

    if (_.isNull(this.state.customCharts)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (this.state.customCharts.length > 0) {
      rows = this.state.customCharts.map(chart => {
        return (
          <tr>
            <td>
              <a href={'/datapoints/charts/' + chart.id + '/'}>{chart.chart_json.title} </a>
              <a href={'/datapoints/charts/' + chart.id + '/edit/'}> edit</a>
            </td>
            <td>{chart.chart_json.type}</td>
            <td><a href={'/datapoints/dashboards/' + chart.dashboard_id}>{chart.dashboard_id}</a></td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-12 columns'>
          <h5 className='all-dashboard'>all custom charts</h5>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Chart Type</th>
                <th>In Dashboard</th>
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

export default ChartsPage
