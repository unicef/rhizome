import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import Dropdown from 'components/atoms/dropdown/DropdownSelect'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

var ChartDropdown = React.createClass({
  propTypes: {
    charts: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    selectChart: React.PropTypes.func.isRequired
  },

  getDefaultProps () {
    return {
      charts: [],
      selected: {'title':'Select existing chart'}
    }
  },

  render () {
    const charts = this.props.charts || []
    const chart_menu_items = this.props.charts.map(chart =>
      <DropdownMenuItem
        key={'chart-' + chart.id}
        text={chart.title}
        onClick={() => this.props.selectChart(chart)}
        classes='chart'
      />
    )

    return (
      <Dropdown
        className='font-weight-600 chart-selector'
        icon='fa-chevron-down'
        text={this.props.selected.title}>
        {chart_menu_items}
      </Dropdown>
    )
  }
})

export default ChartDropdown
