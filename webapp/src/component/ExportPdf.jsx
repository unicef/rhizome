import React from 'react'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string
  },

  defaults: {
    label: 'Export PDF',
    isFetching: false,
    url: '/datapoints/dashboards/export_pdf/?path=',
    interval: 20000
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
    window.setTimeout(this._isCompleteExportDashboard, this.state.interval)
  },

  _isCompleteExportDashboard () {
    if (this.refs.exportFrame.getDOMNode().contentDocument.childElementCount > 0) {
      this.setState({
        label: 'Export PDF',
        isFetching: false,
        href: 'about:blank'
      })
    } else {
      window.setTimeout(this._isCompleteExportDashboard, this.state.interval)
    }
  },

  render () {
    return (
      <div>
        <a role='button' className={this.props.className} onClick={this._onExportDashboard} disabled={this.state.isFetching}>
          {this.state.label}
        </a>
        <iframe width='0' height='0' className='hidden' src={this.state.href} ref='exportFrame'>
          <html>
            <body onload={this._isCompleteExportDashboard}>
            </body>
          </html>
        </iframe>
      </div>
    )
  }
})

export default ExportPdf
