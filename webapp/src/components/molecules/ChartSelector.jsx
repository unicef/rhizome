import React from 'react'
import _ from 'lodash'
import moment from 'moment'

import TitleMenu from 'components/molecules/menus/TitleMenu'
import TitleMenuItem from 'components/molecules/menus/TitleMenuItem'

var ChartSelector = React.createClass({
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
    const chart_menu_items = this.props.charts.map(chart =>
      <TitleMenuItem
        key={'chart-' + chart.id}
        text={chart.title}
        onClick={() => this.props.selectChart(chart)}
        classes='chart'
      />
    )

    return (
      <TitleMenu
        className='font-weight-600 chart-selector'
        icon='fa-chevron-down'
        text={this.props.selected.title}>
        {chart_menu_items}
      </TitleMenu>
    )
  }
})

export default ChartSelector
