import _ from 'lodash'
import React from 'react'

import ChartAPI from 'data/requests/ChartAPI'

var ChartsPage = React.createClass({

  getInitialState () {
    return {
      custom_charts: []
    }
  },

  componentWillMount () {
    ChartAPI.getCharts().then(charts => {
      this.setState({ custom_charts: charts })
    })
  },

  sortCharts (sort_column) {
    let sorted_charts = _.orderBy(this.state.custom_charts, chart => { return chart.id })
    this.setState({ custom_charts: sorted_charts })
  },

  deleteChart (id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      ChartAPI.deleteChart(id).then(response => {
        if (response.status === 204) {
          let remaining_charts = this.state.custom_charts.filter(chart => {
            return chart.id !== id
          })
          this.setState({ custom_charts: remaining_charts })
        }
      })
    }
  },

  render () {
    let rows = <tr><td colSpan='3'>No custom charts created yet.</td></tr>

    if (_.isNull(this.state.custom_charts)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (this.state.custom_charts.length > 0) {
      rows = this.state.custom_charts.map(chart => {
        return (
          <tr>
            <td>
              <a href={'/datapoints/charts/' + chart.id + '/'}>
              <strong>  {chart.chart_json.title}</strong> </a>
            </td>
            <td>{chart.chart_json.type}</td>
            <td>{chart.chart_json.startDate}</td>
            <td>{chart.chart_json.endDate}</td>
            <td>
              <a href={'/datapoints/charts/' + chart.id}>
                <i className='fa fa-pencil'></i> Edit
              </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a onClick={ this.deleteChart.bind(this, chart.id) }>
                <i className='fa fa-trash'></i> Delete
              </a>
            </td>
          </tr>
        )
      })
    }

    return (
      <div className='row'>
        <div className='medium-12 medium-centered columns'>
          <h5 className='all-dashboard'>All Saved Charts</h5>
          <table>
            <thead>
              <tr>
                <th><a onClick={this.sortCharts.bind(this, 'title')}>Title</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'chart')}>Chart Type</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'start')}>Start Date</a></th>
                <th><a onClick={this.sortCharts.bind(this, 'end')}>End Date</a></th>
                <th><a onClick={this.sortCharts.bind(this, '&nbsp')}>&nbsp;</a></th>
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
