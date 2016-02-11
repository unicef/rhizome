import _ from 'lodash'
import React from 'react'

import TitleMenu from '02-molecules/menus/TitleMenu.jsx'
import MenuItem from '02-molecules/MenuItem.jsx'

var RegionTitleMenu = React.createClass({
  propTypes: {
    locations: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      pattern: ''
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return nextProps.locations.length !== this.props.locations.length ||
      nextProps.selected.id !== this.props.selected.id
  },

  _setPattern: function (value) {
    this.setState({ pattern: value })
    this.forceUpdate()
  },

  _buildLocations: function (original_locations, pattern) {
    var locations = original_locations.map(r => {
      return {
        title: r.name,
        value: r.id,
        parent: r.parent_location_id
      }
    })

    if (pattern.length > 2) {
      locations = locations.filter(r => {
        return new RegExp(pattern, 'i').test(r.title)
      })
    } else {
      var idx = _.indexBy(locations, 'value')
      locations = []
      _.each(idx, location => {
        if (idx.hasOwnProperty(location.parent)) {
          var p = idx[location.parent]
          var children = p.children || []

          children.push(location)
          p.children = _.sortBy(children, 'title')
        } else {
          locations.push(location)
        }
      })
    }

    return locations
  },

  render: function () {
    var locations = this._buildLocations(this.props.locations, this.state.pattern)
    var menu_item_components = MenuItem.fromArray(_.sortBy(locations, 'title'), this.props.sendValue)

    return (
      <TitleMenu
        className='font-weight-600 cd-titlebar-margin'
        icon='fa-chevron-down'
        text={this.props.selected.name}
        searchable
        onSearch={this._setPattern}>
        {menu_item_components}
      </TitleMenu>
    )
  }
})

export default RegionTitleMenu
