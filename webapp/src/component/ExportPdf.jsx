import React from 'react'

import api from 'data/api'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string
  },

  defaults: {
    label: 'Export PDF',
    isFetching: false
  },

  getInitialState () {
    return this.defaults
  },

  _onExportDashboard (event) {
    event.preventDefault()

    this.setState({
      label: 'Fetching...',
      isFetching: true
    })

    api.exportPdf(window.location.href).then(res => {
      window.open(`${window.location.origin}/${res.pdfLocation}`)
      this.setState(this.defaults)
    })
  },

  render () {
    return (
      <button className={this.props.className} onClick={this._onExportDashboard} disabled={this.state.isFetching}>
        {this.state.label}
      </button>
    )
  }
})

export default ExportPdf
