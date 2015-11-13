'use strict'

import _ from 'lodash'
import React from 'react'

import TitleMenu from 'component/TitleMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

var RegionTitleMenu = React.createClass({
  propTypes: {
    locations: React.PropTypes.array.isRequired,
    selected: React.PropTypes.object.isRequired,
    sendValue: React.PropTypes.func.isRequired
  },

  getInitialState: function () {
    return {
      filter: ''
    }
  },

  shouldComponentUpdate: function (nextProps, nextState) {
    return nextProps.locations.length !== this.props.locations.length ||
      nextProps.selected.id !== this.props.selected.id
  },

  _setFilter: function (pattern) {
    this.setState({
      filter: pattern
    })
    this.forceUpdate()
  },

  _buildlocations: function (originallocations, filter) {
    var locations = originallocations.map(r => {
      return {
        title: r.name,
        value: r.id,
        parent: r.parent_location_id
      }
    })

    if (filter.length > 2) {
      locations = locations.filter(r => {
        return new RegExp(filter, 'i').test(r.title)
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
    // console.log('RegionTitleMenu RENDER:', this.props.selected)
    var location = this.props.selected.name
    var filter = this.state.filter
    var locations = this._buildlocations(this.props.locations, filter)
    var items = MenuItem.fromArray(_.sortBy(locations, 'title'), this.props.sendValue)

    return (
      <TitleMenu
        className='title-font'
        icon='fa-chevron-down'
        text={location}
        searchable
        onSearch={this._setFilter}>
        {items}
      </TitleMenu>
    )
  }
})

module.exports = RegionTitleMenu
