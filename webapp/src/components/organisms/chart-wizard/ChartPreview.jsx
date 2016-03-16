import React, {PropTypes} from 'react'

const ChartPreview = React.createClass({
  propTypes: {
    chart: PropTypes.shape({
      data: PropTypes.array,
      def: PropTypes.object
    }).isRequired,
    isLoading: PropTypes.bool
  },

  componentWillUpdate(nextProps, nextState) {

    // console.log('---------------------------------------')
    // console.log('')
    // console.log('nextProps', nextProps.chart.data)
    // console.log('this.props', this.props.chart.data)
  },

  // shouldComponentUpdate(nextProps, nextState) {
    // return this.props.chart.data === nextProps.chart.data
  // },

  render () {
    const chart = this.props.chart
    const loading_component = (
      <div className='loading'>
        <i className='fa fa-spinner fa-spin fa-5x'></i>
        <div>Loading</div>
      </div>
    )

    const chart_component = (
      <ul>
        <li>{chart.def.type}</li>
      </ul>
    )

    return (
      <div className='preview-screen'>
        <h3>Preview</h3>
        {!this.props.isLoading ? chart_component : loading_component}
      </div>
    )
  }
})

export default ChartPreview
