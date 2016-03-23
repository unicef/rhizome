import React from 'react'

import TitleMenu from 'components/molecules/menus/TitleMenu.jsx'
import MenuItem from 'components/molecules/MenuItem.jsx'

var ExportPdf = React.createClass({
  propTypes: {
    className: React.PropTypes.string,
    button: React.PropTypes.bool,
    disabled: React.PropTypes.bool
  },

  defaults: {
    label: 'Export',
    disabled: false,
    isFetching: false,
    url: '/export_file/?',
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
    const exportIcon = <i className='fa fa-external-link' style={{fontSize: '1rem', position: 'absolute', top: '1.1rem', left: '1.5rem', color: 'white'}}/>

    let items = MenuItem.fromArray(fileList, this._onExportDashboard)
    let classString = this.props.button ? ' button success ' : ''
    classString += this.state.isFetching ? ' inactive ' : ''
    classString += this.props.className ? this.props.className : ''
    classString += this.props.disabled ? ' disabled ' : ''
    return (
      <div>
        <TitleMenu
          className={'font-weight-600 export-file ' + classString}
          icon={this.props.button ? '' : 'fa-chevron-down'}
          searchable={false}
          text={this.state.label}>
          {items}
        </TitleMenu>
        <iframe width='0' height='0' className='invisible' src={this.state.href}></iframe>
        {this.props.button ? exportIcon : ''}
      </div>
    )
  }
})

export default ExportPdf
