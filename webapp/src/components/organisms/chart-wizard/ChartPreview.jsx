import React from 'react'

const ChartPreview = React.createClass({
  propTypes: {
    isLoading: React.PropTypes.bool,
    children: React.PropTypes.element
  },

  render () {
    let loading = (
      <div className='loading'>
        <i className='fa fa-spinner fa-spin fa-5x'></i>
        <div>Loading</div>
      </div>
    )

    return (
      <div className='preview-screen'>
        <h3>Preview</h3>
        {this.props.isLoading ? loading : this.props.children}
      </div>
    )
  }
})

export default ChartPreview
