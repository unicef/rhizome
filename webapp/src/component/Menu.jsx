import _ from 'lodash'
import React from 'react'

import Search from 'component/Search.jsx'

import dom from 'util/dom'

export default React.createClass({
  propTypes: {
    onSearch: React.PropTypes.func,
    onBlur: React.PropTypes.func,
    searchable: React.PropTypes.bool,
    x: React.PropTypes.number,
    y: React.PropTypes.number,
    children: React.PropTypes.array,
    search: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.bool
    ])
  },

  getDefaultProps: function () {
    return {
      onSearch: _.noop,
      onBlur: _.noop,
      searchable: false,
      x: 0,
      y: 0
    }
  },

  getInitialState: function () {
    return {
      maxHeight: 'none',
      marginLeft: 0,
      orientation: 'center',
      pattern: ''
    }
  },

  componentDidMount: function () {
    window.addEventListener('resize', this._onResize)

    this._onResize()
    if (this.props.search) {
      React.findDOMNode(this.refs.search).focus()
    } else {
      React.findDOMNode(this).focus()
    }
  },

  componentDidUpdate: function () {
    // @john you can console here and try to search when choosing an indicator in custom dashboard, then this method will be called.
    // And the dropdown list will be re-positioned by _onResize method.
    // So the Math.floor method have fixed the max stack overflow issue when searching for an indicator.
    // If you commented the Math.floor method, then try to search, you will see the max stack overflow error.
    this._onResize()
  },

  componentWillUnmount: function () {
    window.removeEventListener('resize', this._onResize)
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    // @john we check this.state here to fix the position of the dropdown list.
    // If this.state is not equal to nextState, then will go to componentDidUpdate, then _onResize method.
    return !_.isEqual(nextProps, this.props) || !_.isEqual(nextState, this.state)
  },

  _onResize: function () {
    var menu = dom.dimensions(React.findDOMNode(this.refs.menu))
    var items = (this.refs.itemlist ? dom.dimensions(React.findDOMNode(this.refs.itemlist)) : {height: 0})

    // Compute offset relative to the viewport
    var x = this.props.x - window.pageXOffset
    var y = this.props.y - window.pageYOffset

    // Default position is centered
    var orientation = 'center'
    var marginLeft = -menu.width / 2

    // Calculate the edges based on a centered menu
    var rightEdge = x + (menu.width / 2)
    var leftEdge = x - (menu.width / 2)

    if (menu.width > window.innerWidth || leftEdge < 0) {
      orientation = 'left'
      marginLeft = 0
    } else if (rightEdge > window.innerWidth) {
      orientation = 'right'
      marginLeft = 0
    }

    this.setState({
      orientation: orientation,
      maxHeight: Math.floor(window.innerHeight - y - (menu.height - items.height)),
      marginLeft: Math.floor(marginLeft)
    })
  },

  render: function () {
    var itemlistStyle = { maxHeight: this.state.maxHeight }
    var containerStyle = { marginLeft: this.state.marginLeft }
    var position = {
      position: 'absolute',
      left: this.props.x,
      top: this.props.y
    }

    var search = this.props.searchable
      ? (<Search onChange={this.props.onSearch} onBlur={this.onBlur} />)
      : null

    return (
      <div className='menu' style={position} tabIndex='-1' onBlur={this.onBlur}>
        <div className={this.state.orientation + ' container'}
          style={containerStyle}
          ref='menu'>

          <div className='background'>
            <div className='arrow'></div>
            {search}
            <ul ref='itemlist' style={itemlistStyle}>
              {this.props.children}
            </ul>
          </div>

        </div>
      </div>
    )
  },

  onBlur: function () {
    var self = this

    window.setTimeout(function () {
      var menu = React.findDOMNode(self)

      if (!dom.parentOf(menu, document.activeElement)) {
        self.props.onBlur()
      }
    })
  }
})
