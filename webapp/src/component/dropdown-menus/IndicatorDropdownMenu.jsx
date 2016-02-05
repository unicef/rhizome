import _ from 'lodash'
import React from 'react'

import DropdownMenu from 'component/dropdown-menus/DropdownMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

function filterMenu (items, pattern) {
  if (_.size(pattern) < 4) {
    return items
  }

  var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))
  var itemList = _(items).map(match).flatten().value()

  return _.uniq(itemList, (item) => { return item.id })
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

var IndicatorDropdownMenu = React.createClass({
  propTypes: {
    indicators: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    style: React.PropTypes.string
  },

  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  render: function () {
    var self = this
    if (this.props.indicators.length === 0) {
      return (<button className={'button ' + this.props.style}><i className='fa fa-spinner fa-spin'></i> Loading Indicators...</button>)
    }

    var indicators = MenuItem.fromArray(filterMenu(this.props.indicators, this.state.pattern), self.props.sendValue)

    var props = _.omit(this.props, 'indicators', 'sendValue')

    return (
      <DropdownMenu
        style={this.props.style}
        searchable
        onSearch={this._setPattern}
        {...props}>
        {indicators}
      </DropdownMenu>
    )
  },

  _setPattern: function (value) {
    this.setState({pattern: value})
  }
})

export default IndicatorDropdownMenu
