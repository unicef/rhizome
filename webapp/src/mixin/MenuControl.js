import _ from 'lodash'
import React from 'react'
import Layer from 'react-layer'

import Menu from 'component/menus/Menu.jsx'
import dom from 'util/dom'

var MenuControl = {
  getDefaultProps: function () {
    return {
      style: '',
      searchable: true,
      onSearch: _.noop
    }
  },

  getInitialState: function () {
    return {
      open: false,
      pattern: ''
    }
  },

  componentDidUpdate: function () {
    if (this.state.open) {
      var offset = dom.documentOffset(React.findDOMNode(this))
      var x = (offset.right + offset.left) / 2

      var menu = (
        <Menu x={x} y={offset.bottom}
          onBlur={this.close}
          onSearch={this.props.onSearch}
          searchable={this.props.searchable}
          children={this.props.children}/>
      )

      if (!this.layer) {
        this.layer = new Layer(document.body, function () {
          return menu
        })

        window.addEventListener('keyup', this)
      } else {
        // Here's a gross way to re-render the menu when its items have changed
        // (due, for example, to them being filtered) without destroying and
        // recreating the layer every time.
        this.layer._render = function () { return menu }
      }

      this.layer.render()
    } else if (this.layer) {
      this.layer.destroy()
      this.layer = null

      // Clear out the search patterns that the parent component is necessarily
      // using to provide filtered menu items.
      this.props.onSearch('')
      window.removeEventListener('keyup', this)
    }
  },

  _toggleMenu: function () {
    this.setState({ open: !this.state.open })
  },

  filterMenu: function (items, pattern) {
    if (_.size(pattern) < 3) return items

    var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'), this)

    return _(items).map(match).flatten().value()
  },

  handleEvent: function (evt) {
    switch (evt.type) {
      case 'keyup':
        if (evt.keyCode === 27) {
          this.close()
        }
        break
      default:
        break
    }
  },

  close: function () {
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

export default MenuControl
