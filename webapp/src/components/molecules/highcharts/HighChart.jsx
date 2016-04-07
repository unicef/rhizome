import _ from 'lodash'
import React, { Component, PropTypes } from 'react'
import format from 'utilities/format'
import palettes from 'utilities/palettes'

import ChartFactory from 'components/molecules/highcharts/ChartFactory'

class HighChart extends Component {

  getSeries () { console.info('------ HighChart.getData')
    const data = this.props.datapoints.melted
    const groupByIndicator = this.props.groupBy === 'indicator'
    const grouped_data = groupByIndicator ? _.groupBy(data, 'indicator.id') : _.groupBy(data, 'location.id')
    const series = []
    _.forEach(grouped_data, group => {
      _.sortBy(group, _.method('campaign.start_date.getTime'))
      series.push({
        name: groupByIndicator ? group[0].indicator.name : group[0].location.name,
        data: group.map(datapoint => datapoint.value) // Needs to be sorted by date
      })
    })
    return series
  }

  render () { console.info('------ HighChart.render')
    this.data.colors = palettes[this.props.palette]
    this.data.series = this.getSeries()
    return (
      <div id='highchart-container'>
        <ChartFactory config={this.data} map={this.props.type === 'MapChart'} isPureConfig/>
      </div>
    )
  }
}

export default HighChart

