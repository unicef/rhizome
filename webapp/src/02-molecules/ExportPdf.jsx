import React from 'react'

import TitleMenu from '02-molecules/menus/TitleMenu.jsx'
import MenuItem from '02-molecules/MenuItem.jsx'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string
  },

  defaults: {
    label: 'Export',
    isFetching: false,
    url: '/dashboards/export_file/?',
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

  _onExportDashboard (fileType) {
    var type = 'type=' + fileType
    var path = 'path=' + window.location.href
    this.setState({
      label: 'Fetching...',
      isFetching: true,
      href: this.state.url + type + '&' + path
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
    fileList.push({value: 'pdf', title: 'PDF'})
    fileList.push({value: 'jpeg', title: 'IMAGE'})

    let items = MenuItem.fromArray(fileList, this._onExportDashboard)

    return (
      <div>
        <TitleMenu
          className={'font-weight-600 ' + this.props.className + (this.state.isFetching ? ' inactive' : '')}
          icon='fa-chevron-down'
          text={this.state.label}>
          {items}
        </TitleMenu>
        <iframe width='0' height='0' className='invisible' src={this.state.href}></iframe>
      </div>
    )
  }
})

export default ExportPdf
