import React from 'react'

export default React.createClass({
  propTypes: {
    charts: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired
  },

  _handleChange (event) {
    this.props.onChange(event.target.value)
  },

  render () {
    var chartBoxes = this.props.charts.map((chart, index) => {
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
})
