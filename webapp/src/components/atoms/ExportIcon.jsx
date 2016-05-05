import React from 'react'

import IconButtonDropdown from 'components/atoms/buttons/IconButtonDropdown'
import Dropdown from 'components/atoms/selectors/DropdownSelector'
import MenuItem from 'components/molecules/MenuItem'

var ExportIcon = React.createClass({
  propTypes: {
    className: React.PropTypes.string,
    button: React.PropTypes.bool,
    disabled: React.PropTypes.bool,
    exportPath: React.PropTypes.string
  },

  getDefaultProps() {
    return {
      disabled: false,
      exportPath: window.location.pathname
    }
  },

  getInitialState () {
    return {
      label: 'Export',
      disabled: false,
      iconOnly: false,
      isFetching: false,
      url: '/export_file/?',
      interval: 1000,
      cookieName: 'fileDownloadToken'
    }
  },

  selectOption (option) {
    console.log('ExportIcon.selectOption')
    if (option === 'csv') {
      this.downloadRawData()
    } else {
      this.exportImage(option)
    }
  },

  // EXPORT CSV
  //---------------------------------------------------------------------------
  downloadRawData () {
    console.log('ExportIcon.downloadRawData')
    if (!this.props.enable || this.state.isWorking) return
    let url = this.props.onClick()
    this.setState({
      url: url,
      isWorking: true
    })
    // var self = this
    var refreshIntervalId = window.setInterval(() => {
      // var cookieValue = self._getCookie(self.props.cookieName)
      // if (cookieValue === 'true') {
        this.completeDownload(refreshIntervalId)
      // }
    }, 1000)
  },

  completeDownload (refreshIntervalId) {
    console.log('ExportIcon.completeDownload')
    this.setState({
      isWorking: false,
      url: 'about:blank'
    })
    document.cookie = this.props.cookieName + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    window.clearInterval(refreshIntervalId)
  },


  // EXPORT IMAGE
  //---------------------------------------------------------------------------
  exportImage (fileType) {
    console.log('ExportIcon.exportImage')
    console.log('fileType', fileType)
    var type = 'type=' + fileType
    var path = 'path=' + window.location.origin + this.props.exportPath
    console.log('window.location', window.location)
    console.log('window.location.href', window.location.href)
    console.log('path', path)
    this.setState({
      label: 'Fetching...',
      isFetching: true,
      href: this.state.url + type + '&' + path
    })
    var self = this
    var refreshIntervalId = window.setInterval(() => {
      var cookieValue = self._getCookie(self.state.cookieName)
      if (cookieValue === 'true') {
        this.completeExportImage(refreshIntervalId)
      }
    }, this.state.interval)
  },

  completeExportImage (refreshIntervalId) {
    this.setState({
      label: 'Export To ',
      isFetching: false,
      href: 'about:blank'
    })
    document.cookie = this.state.cookieName + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    window.clearInterval(refreshIntervalId)
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

  render () {
    let classString = this.props.button ? ' button success ' : ''
    classString += this.state.isFetching ? ' inactive ' : ''
    classString += this.props.className ? this.props.className : ''
    classString += this.props.disabled ? ' disabled ' : ''

    return (
      <span style={{position: 'relative', top: '1px', left: '4px'}}>
        <IconButtonDropdown classes={classString} searchable={false} icon='fa-external-link' text='Export'>
          <MenuItem key='jpeg' value='jpeg' title='Export as IMAGE' sendValue={this.selectOption} />
          <MenuItem key='pdf' value='pdf'  title='Export as PDF' sendValue={this.selectOption} />
          <MenuItem key='csv' value='csv'  title='Export as CSV' sendValue={this.selectOption} />
        </IconButtonDropdown>
        <iframe width='0' height='0' className='invisible' src={this.state.href}></iframe>
      </span>
    )
  }
})

export default ExportIcon
