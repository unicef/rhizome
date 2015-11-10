var React = require('react')

module.exports = React.createClass({
  propTypes: {
    charts: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired
  },
  _handleChange: function (event){
    this.props.onChange(event.target.value)
  },
  render: function (){
    var self = this
    var chartBoxes = this.props.charts.map(function (chart, index){
      return (
        <div key={chart.name} className={'chart-box-wrapper ' + (chart.name === self.props.value ? 'active' : '')}>
          <div className='chart-box' onClick={self.props.onChange.bind(null, chart.name)}>
            <img className='chart-icon' src={'/static/img/chart-icons/' + chart.name + '.png'} />
            {chart.name}
          </div>
        </div>
      )
    })
    return (<div className='chart-select'>{chartBoxes}</div>)
  }
})
