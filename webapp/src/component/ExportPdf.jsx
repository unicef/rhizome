import React from 'react'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string
  },

  defaults: {
    label: 'Export PDF',
    isFetching: false,
    url: '/datapoints/dashboards/export_pdf/?path=',
    interval: 15000
  },

  getInitialState () {
    return this.defaults
  },

  _onExportDashboard () {
    this.setState({
      label: 'Fetching...',
      isFetching: true,
      href: this.state.url + window.location.href
    })
    window.setTimeout(this._onCompleteExportDashboard, this.state.interval)
  },

  _onCompleteExportDashboard () {
    console.log('finish')
    this.setState({
      label: 'Export PDF',
      isFetching: false
    })
  },

  render () {
    return (
      <div>
        <button className={this.props.className} onClick={this._onExportDashboard} disabled={this.state.isFetching}>
          {this.state.label}
        </button>
        <iframe width='0' height='0' className='hidden' src={this.state.href}></iframe>
      </div>
    )
  }
})

export default ExportPdf
