import React, {Component, PropTypes} from 'react'

import Dropdown from 'components/atoms/select/Select'
import DropdownMenuItem from 'components/atoms/dropdown/DropdownMenuItem'

class ChartSelect extends Component {

  static propTypes = {
    charts: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    selectChart: React.PropTypes.func.isRequired
  }

  static defaultProps = {
    charts: [],
    selected: {'title': 'Select existing chart'}
  }

  render () {
    const charts = this.props.charts || []
    const chart_menu_items = charts.map(chart =>
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
}

export default ChartSelect
