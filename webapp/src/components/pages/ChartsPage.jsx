import _ from 'lodash'
import uuid from 'uuid'
import orderBy from 'lodash.orderby'
import React from 'react'
import Reflux from 'reflux'

import ChartAPI from 'data/requests/ChartAPI'
import ChartActions from 'actions/ChartActions'
import ChartStore from 'stores/ChartStore'


var ChartsPage = React.createClass({

  mixins: [
    Reflux.connect(ChartStore, 'charts'),
  ],

  getInitialState() {
    return {
      sort_column: null,
      sort_desc: true
    }
  },

  sortCharts (sort_column) {
    if (sort_column === this.state.sort_column) {
      this.setState({sort_desc: !this.state.sort_desc})
    } else {
      this.setState({sort_column: sort_column})
    }
  },

  duplicateChart (chart) {
    const chart_def = chart.chart_json
    ChartActions.postChart({
      title: chart.title + ' Copy',
      uuid: uuid.v4(),
      chart_json: JSON.stringify({
        type: chart_def.type,
        start_date: chart_def.start_date,
        end_date: chart_def.end_date,
        campaign_ids: chart_def.campaign_ids,
        location_ids: chart_def.location_ids,
        indicator_ids: chart_def.indicator_ids
      })
    })
  },

  deleteChart (id) {
    if (confirm('Are you sure you want to delete this chart?')) {
      ChartActions.deleteChart(id)
    }
  },


  render () {
    let rows = <tr><td colSpan='3'>No custom charts created yet.</td></tr>
    if (_.isNull(this.state.charts.list)) {
      rows = <tr><td><i className='fa fa-spinner fa-spin'></i> Loading&hellip;</td></tr>
    } else if (this.state.charts.list.length > 0) {
      const order = this.state.sort_desc ? 'desc' : 'asc'
      const chart_list = orderBy(this.state.charts.list, this.state.sort_column, order)
      rows = chart_list.map(chart => {
        return (
          <tr>
            <td>
              <a href={'/charts/' + chart.id + '/'}>
              <strong>  {chart.title}</strong> </a>
            </td>
            <td>{chart.chart_json.type}</td>
            <td>{chart.chart_json.start_date}</td>
            <td>{chart.chart_json.end_date}</td>
            <td>
              <a onClick={() => this.duplicateChart(chart)}>
                <i className='fa fa-clone'></i> Duplicate
              </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a href={'/charts/' + chart.id + '/edit'}>
                <i className='fa fa-pencil'></i> Edit
              </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              <a onClick={() => this.deleteChart(chart.id) }>
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
          <h2 className='all-dashboard left'>All Saved Charts</h2>
          <a href='/charts/create' className='button success right'>Create New Chart</a>
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
