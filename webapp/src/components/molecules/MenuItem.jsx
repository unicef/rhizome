import React from 'react'
import _ from 'lodash'

var MenuItem = React.createClass({
  propTypes: {
    sendValue: React.PropTypes.func.isRequired,
    title: React.PropTypes.string.isRequired,
    value: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number
    ]),
    classes: React.PropTypes.string,
    ancestryString: React.PropTypes.string,
    children: React.PropTypes.array,
    depth: React.PropTypes.number,
    disabled: React.PropTypes.bool,
    filtered: React.PropTypes.bool,
    displayTitle: React.PropTypes.string,
    noValue: React.PropTypes.bool,
    hideLastLevel: React.PropTypes.bool // Don't show any children if they have no children themselves
  },

  statics: {
    fromArray: function (arr, sendValue, depth) {
      if (!_.isFinite(depth)) {
        depth = 0
      }
      return arr.map(item => <MenuItem key={item.value} depth={depth} sendValue={sendValue} {...item} />)
    }
  },

  getDefaultProps: function () {
    return {
      depth: 0,
      filtered: false,
      hideLastLevel: false,
      displayTitle: null
    }
  },

  getInitialState: function () {
    return {
      open: false,
      disabled: false
    }
  },

  componentDidMount() {
    this.setState({disabled: this.props.disabled})
  },

  componentWillUpdate(nextProps, nextState) {
    if (this.props.disabled !== nextProps.disabled) {
      this.setState({disabled: nextProps.disabled})
    }
  },

  _toggleChildren: function (e) {
    e.stopPropagation()
    this.setState({open: !this.state.open})
  },

  _handleClick: function (e) {
    if (!this.props.noValue && !this.state.disabled) {
      this.props.sendValue(this.props.value)
      this.setState({disabled: true})
    } else {
      this._toggleChildren(e)
    }
  },

  render: function () {
    const props = this.props
    var hasChildren = !props.filtered && _.isArray(props.children) && props.children.length > 0
    var isLastParent = props.children && props.children.filter(child => child.children).length < 1
    console.log('------------------------------------------------------')
    console.log('isLastParent', isLastParent)
    console.log('this.propsHideLastLevel', props.hideLastLevel)
    const hideArrow = isLastParent && props.hideLastLevel
    console.log('hideArrow', hideArrow)
    var prefix = props.filtered ? _.get(this.props, 'ancestryString', '') : ''
    var title = prefix + (props.displayTitle === null ? props.title : props.displayTitle)

    var children = null
    if (props.children && this.state.open) {
      children = props.children.map(item => {
        return <MenuItem key={item.value} depth={props.depth+1} sendValue={props.sendValue} {...item} hideLastLevel={props.hideLastLevel}/>
      })
    }

    var arrowStyle = {
      paddingLeft: this.state.filtered ? '5px' : (5 + (17 * props.depth)) + 'px',
      textDecoration: this.state.disabled ? 'line-through' : null,
      display: 'inline-block'
    }
    const arrow_button = hasChildren ? (
      <a onClick={this._toggleChildren} className={hasChildren ? 'folder' : null} style={arrowStyle}>
        <i className={'fa fa-lg fa-fw fa-caret-' + (this.state.open ? 'down' : 'right')}></i>
      </a>
    ) : null

    var itemStyle = {
      textDecoration: this.state.disabled ? 'line-through' : null,
      display: 'inline-block'
    }
    !hasChildren || hideArrow ?  itemStyle.paddingLeft = this.state.filtered ? '5px' : (15 + (18 * props.depth)) + 'px' : null
    const item_button = (
      <a role='menuitem' onClick={this._handleClick} style={itemStyle} tabIndex='-1' className={hasChildren ? 'folder' : null} >
        {title}
      </a>
    )

    return (
      <li className={props.classes}>
        { hideArrow ? null : arrow_button }
        { item_button }
        <div>
          {children}
        </div>
      </li>
    )
  }
})

export default MenuItem
