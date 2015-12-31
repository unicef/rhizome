import React from 'react'

import TitleMenu from 'component/TitleMenu.jsx'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string,
    fileType: React.PropTypes.string
  },

  defaults: {
    label: 'Export To ',
    isFetching: false,
    url: '/datapoints/dashboards/export_file/?',
    interval: 1000,
    cookieName: 'fileDownloadToken'
  },

  getInitialState () {
    return this.defaults
  },

  _getCookie (name) {
    if (document.cookie.length > 0) {
      var c_start = document.cookie.indexOf(name + '=')
      if (c_start !== -1) {
        c_start = c_start + name.length + 1
        var c_end = document.cookie.indexOf(';', c_start)
        if (c_end === -1) {
          c_end = document.cookie.length
        }
        return document.cookie.substring(c_start, c_end)
      }
    }
    return ''
  },

  _onExportDashboard () {
    var fileType = 'type=' + this.props.fileType
    var path = 'path=' + window.location.href
    this.setState({
      label: 'Fetching ',
      isFetching: true,
      href: this.state.url + fileType + '&' + path
    })
    var self = this
    var refreshIntervalId = window.setInterval(() => {
      var cookieValue = self._getCookie(self.state.cookieName)
      if (cookieValue === 'true') {
        this._isCompleteExportDashboard(refreshIntervalId)
      }
    }, this.state.interval)
  },

  _isCompleteExportDashboard (refreshIntervalId) {
    this.setState({
      label: 'Export To ',
      isFetching: false,
      href: 'about:blank'
    })
    document.cookie = this.state.cookieName + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    window.clearInterval(refreshIntervalId)
  },

  render () {
    var fileList = []
    if (waffle.switch_is_active('pdf')) {
      fileList.push({key: 'PDF'})
    }

    if (waffle.switch_is_active('image')) {
      fileList.push({key: 'IMAGE'})
    }

    let items = fileList.map((type) => {
      return (
        <li>
          <a role='menuitem' className={this.props.className + (this.state.isFetching ? ' inactive' : '')} onClick={this._onExportDashboard}>
            {type.key}
          </a>
        </li>)
    })

    return (
      <div>
        <TitleMenu
          className={'font-weight-600 ' + this.props.className + (this.state.isFetching ? ' inactive' : '')}
          icon='fa-chevron-down'
          text='Export to'>
          {items}
        </TitleMenu>
        <iframe width='0' height='0' className='hidden' src={this.state.href}></iframe>
      </div>
    )
  }
})

export default ExportPdf
