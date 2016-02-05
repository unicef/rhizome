import _ from 'lodash'
import React from 'react'

import DropdownMenu from 'component/dropdown-menus/DropdownMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

function filterMenu (items, pattern) {
  if (!pattern || pattern.length < 3) {
    return items
  }

  var match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))

  return _(items).map(match).flatten().value()
}

function findMatches (item, re) {
  var matches = []

  if (re.test(_.get(item, 'title'))) {
    matches.push(_.assign({}, item, {filtered: true}))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

var LocationsDropDownMenu = React.createClass({

  propTypes: {
    locations: React.PropTypes.array.isRequired,
    sendValue: React.PropTypes.func.isRequired,
    style: React.PropTypes.string,
    text: React.PropTypes.string
  },

  getInitialState: function () {
    return {
      locationSearch: ''
    }
  },

  setLocationSearch: function (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  render: function () {
    if (this.props.locations.length === 0) {
      return (<button className={'button ' + this.props.style}><i className='fa fa-spinner fa-spin'></i> Loading Locations...</button>)
    }

    var locations = MenuItem.fromArray(filterMenu(this.props.locations, this.state.locationSearch), this.props.sendValue)

    return (
      <DropdownMenu
        icon='fa-globe'
        text={this.props.text}
        style={this.props.style}
        searchable
        onSearch={this.setLocationSearch}>
        {locations}
      </DropdownMenu>
    )
  }
})

export default LocationsDropDownMenu
