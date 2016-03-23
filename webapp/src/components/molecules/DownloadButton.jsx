import React from 'react'

var DownloadButton = React.createClass({
  propTypes: {
    data: React.PropTypes.array,
    onClick: React.PropTypes.func.isRequired,
    enable: React.PropTypes.bool,
    text: React.PropTypes.string.isRequired,
    cookieName: React.PropTypes.string.isRequired,
    working: React.PropTypes.string.isRequired,
    classes: React.PropTypes.string
  },

  defaults: {
    isWorking: false,
    url: 'about:blank'
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

  _download () {
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
        this._completeDownload(refreshIntervalId)
      // }
    }, 1000)
  },

  _completeDownload (refreshIntervalId) {
    this.setState({
      isWorking: false,
      url: 'about:blank'
    })
    document.cookie = this.props.cookieName + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'
    window.clearInterval(refreshIntervalId)
  },

  render () {
    let text = this.state.isWorking ? this.props.working : this.props.text
    let classesString = this.props.enable && !this.state.isWorking ? 'button success expand ' : 'button success expand disabled '
    return (
      <button role='button'
        className={classesString + this.props.classes}
        onClick={this._download}>
        <i className='fa fa-fw fa-download' />&emsp; {text}
        <iframe width='0' height='0' className='hidden' src={this.state.url}></iframe>
      </button>
    )
  }
})

export default DownloadButton
