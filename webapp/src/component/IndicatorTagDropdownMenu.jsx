'use strict'

var _ = require('lodash')
var React = require('react')
var moment = require('moment')

var DropdownMenu = require('component/DropdownMenu.jsx')
var MenuItem = require('component/MenuItem.jsx')

function findMatches (item, re) {
  var matches = []

  if (re.test(_.get(item, 'title'))) {
    matches.push(_.assign({}, item, { filtered: true }))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

function filterMenu (items, pattern) {
  if (_.size(pattern) < 3) {
    return items
  }

  var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))

  return _(items).map(match).flatten().value()
}

var IndicatorTagDropdownMenu = React.createClass({
  propTypes: {
    tag_tree: React.PropTypes.array.isRequired,
    text: React.PropTypes.string.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return nextProps.text !== this.props.text
  },

  render: function () {
    var self = this

    if (this.props.tag_tree.length === 0) {
      return (<button className='tiny'><i className='fa fa-spinner fa-spin'></i> Loading Tags...</button>)
    }

    var tag_tree = MenuItem.fromArray(filterMenu(this.props.tag_tree, this.state.pattern), self.props.sendValue)
    var props = _.omit(this.props, 'tag_tree', 'sendValue')
    var selected_name = this.props.text // this is a name not an object!

    return (
      <DropdownMenu
        searchable
        text={selected_name}
        onSearch={this._setPattern}
        {...props}>
        {tag_tree}
      </DropdownMenu>
    )
  },

  _setPattern: function (value) {
    this.setState({ pattern: value })
  }
})

module.exports = IndicatorTagDropdownMenu
