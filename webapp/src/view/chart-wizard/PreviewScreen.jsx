import React from 'react'

let PreviewScreen = React.createClass({
  propTypes: {
    isLoading: React.PropTypes.bool
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
        <h1>Preview</h1>
        {this.props.isLoading ? loading : this.props.children}
      </div>
    )
  }
})

export default PreviewScreen
