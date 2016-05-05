import React, {Component, PropTypes} from 'react'

import builderDefinitions from 'components/molecules/charts/utils/builderDefinitions'

class ChartTypeSelect extends Component {

  static propTypes = {
    value: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number
    ]),
    onChange: React.PropTypes.func.isRequired
  }

  _handleChange (event) {
    this.props.onChange(event.target.value)
  }

  render () {
    const charts = builderDefinitions.charts
    var chartBoxes = charts.map((chart, index) => {
      return (
        <div key={chart.name} className={'chart-box-wrapper ' + (chart.name === this.props.value ? 'active' : '')}>
          <div className='chart-box' onClick={this.props.onChange.bind(null, chart.name)}>
            <img className='chart-icon' src={'/static/img/chart-icons/' + chart.name + '.png'} />
            <p>{chart.name}</p>
          </div>
        </div>
      )
    })
    return (<div className='chart-select'>{chartBoxes}</div>)
  }
}

export default ChartTypeSelect
