import _ from 'lodash'
import ReactDOM from 'react-dom'
import React, {Component, PropTypes} from 'react'
import Layer from 'react-layer'

import DropdownMenu from 'components/dropdown/DropdownMenu'
import dom from 'utilities/dom'

class Dropdown extends Component {

  constructor (props) {
    super(props)
    this.state = {
      items: [],
      open: false,
      pattern: ''
    }
  }

  static defaultProps = {
    style: '',
    searchable: true
  }

  componentDidUpdate = () => {
    if (this.state.open) {
      var offset = dom.documentOffset(ReactDOM.findDOMNode(this))
      var x = (offset.right + offset.left) / 2

      var menu = (
        <DropdownMenu x={x} y={offset.bottom}
          onBlur={this.close}
          onSearch={this._setPattern}
          searchable={this.props.searchable}
          children={this.items || this.props.items}/>
      )

      if (!this.layer) {
        this.layer = new Layer(document.body, () => menu)

        window.addEventListener('keyup', this)
      } else {
        // Here's a gross way to re-render the menu when its items have changed
        // (due, for example, to them being filtered) without destroying and
        // recreating the layer every time.
        this.layer._render = () => menu
      }
      this.layer.render()
    } else if (this.layer) {
      this.layer.destroy()
      this.layer = null

      // Clear out the search patterns that the parent component is necessarily
      // using to provide filtered menu items.
      this._setPattern('')
      window.removeEventListener('keyup', this)
    }
  }

  filterMenu = (items, pattern) => {
    if (_.size(pattern) < 3) return items

    var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'), this)

    return _(items).map(match).flatten().value()
  }

  handleEvent = (evt) => {
    switch (evt.type) {
      case 'keyup':
        if (evt.keyCode === 27) {
          this.close()
        }
        break
      default:
        break
    }
  }

  _toggleMenu = (e) => {
    if (e) {
      e.preventDefault()
    }
    this.setState({ open: !this.state.open })
  }

  _setPattern = (value) => {
    this.setState({ pattern: value })
  }

  close = () => {
    console.log('close!')
    this.setState({ open: false })
  }
}



function findMatches (item, re) {
  var matches = []
  if (re.test(_.get(item, 'value')) && item.noValue !== true) {
    matches.push(_.assign({}, item, {filtered: true}))
  }
  if (re.test(_.get(item, 'title')) && item.noValue !== true) {
    matches.push(_.assign({}, item, {filtered: true}))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

export default Dropdown
