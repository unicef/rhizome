import React from 'react'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string,
    href: '#'
  },

  defaults: {
    label: 'Export PDF',
    isFetching: false,
    url: '/datapoints/dashboards/export_pdf/?path='
  },

  getInitialState () {
    return this.defaults
  },

  _onExportDashboard () {
    this.setState({
      label: 'Fetching...',
      isFetching: true
    })

    this.props.href = this.state.url + window.location.href
  },

  render () {
    return (
      <a role='button' className={this.props.className} onClick={this._onExportDashboard} href={this.props.href} disabled={this.state.isFetching}>
        {this.state.label}
      </a>
    )
  }
})

export default ExportPdf
