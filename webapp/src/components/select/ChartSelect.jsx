import React, {Component, PropTypes} from 'react'

import Select from 'components/select/Select'
import DropdownMenuItem from 'components/dropdown/DropdownMenuItem'

class ChartSelect extends Component {

  constructor (props) {
    super(props)
    this.state = {
      pattern: ''
    }
  }

  static propTypes = {
    charts: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    selectChart: React.PropTypes.func.isRequired
  }

  static defaultProps = {
    charts: [],
    selected: {'title': 'Select existing chart'}
  }

  setPattern = (value) => {
    this.setState({ pattern: value })
    this.forceUpdate()
  }

  render () {
    const charts = this.props.charts || []
    const pattern = this.state.pattern
    const filtered_charts = pattern.length > 2 ? charts.filter(chart => new RegExp(pattern, 'i').test(chart.title)) : charts
    const chart_menu_items = filtered_charts.map(chart =>
      <DropdownMenuItem
        key={'chart-' + chart.id}
        text={chart.title}
        onClick={() => this.props.selectChart(chart)}
        classes='chart'
      />
    )

    return (
      <Select
        className='font-weight-600 chart-selector'
        icon='fa-chevron-down'
        text={this.props.selected.title}
        searchable
        onSearch={this.setPattern}>
        {chart_menu_items}
      </Select>
    )
  }
}

export default ChartSelect
