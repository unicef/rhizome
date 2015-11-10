var _ = require('lodash')
var React = require('react')

var Search = require('component/Search.jsx')

var dom = require('util/dom')

module.exports = React.createClass({
  propTypes : {
    onSearch   : React.PropTypes.func,
    onBlur     : React.PropTypes.func,
    searchable : React.PropTypes.bool,
    x          : React.PropTypes.number,
    y          : React.PropTypes.number
  },

  getDefaultProps : function () {
    return {
      onSearch   : _.noop,
      onBlur     : _.noop,
      searchable : false,
      x          : 0,
      y          : 0
    }
  },

  getInitialState: function (){
     return {
       maxHeight   : 'none',
       marginLeft  : 0,
       orientation : 'center',
       pattern     : ''
     }
  },

  componentDidMount: function (){
    window.addEventListener('resize', this._onResize)

    this._onResize()
    if (this.props.search) {
      React.findDOMNode(this.refs.search).focus()
    } else {
      React.findDOMNode(this).focus()
    }
  },

  componentDidUpdate : function () {
    this._onResize()
  },

  componentWillUnmount : function () {
    window.removeEventListener('resize', this._onResize)
  },

  shouldComponentUpdate : function (nextProps, nextState) {
    return !_.isEqual(nextProps, this.props) || !_.isEqual(nextState, this.state)
  },

  _onResize : function () {
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
      orientation : orientation,
      maxHeight   : window.innerHeight - y - (menu.height - items.height),
      marginLeft  : marginLeft
    })
  },

  render: function (){
    var itemlistStyle = { maxHeight : this.state.maxHeight }
    var containerStyle = { marginLeft : this.state.marginLeft }
    var position = {
      position : 'absolute',
      left     : this.props.x,
      top      : this.props.y
    }

    var search = this.props.searchable ?
      (<Search onChange={this.props.onSearch} onBlur={this.onBlur} />) :
      null

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

  onBlur : function () {
    var self = this

    window.setTimeout(function () {
      var menu = React.findDOMNode(self)

      if (!dom.parentOf(menu, document.activeElement)) {
        self.props.onBlur()
      }
    })
  }
})
