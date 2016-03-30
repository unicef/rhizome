import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import List from 'components/molecules/list/List'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import RegionTitleMenu from 'components/molecules/menus/RegionTitleMenu'

const LocationSelector = React.createClass({

  propTypes: {
    locations: PropTypes.shape({
      raw: PropTypes.array,
      list: PropTypes.array
    }).isRequired,
    selected_locations: PropTypes.array,
    setLocations: PropTypes.func,
    selectLocation: PropTypes.func,
    deselectLocation: PropTypes.func,
    clearSelectedLocations: PropTypes.func,
    classes: PropTypes.string,
    multi: PropTypes.bool
  },

  getDefaultProps() {
    return {
      selected_locations: []
    }
  },

  getAvailableLocations () {
    const selected_ids = this.props.selected_locations.map(location => location.id)
    const locations_filtered = this.props.locations.filtered
    locations_filtered.forEach(country => {
      country.disabled = selected_ids.indexOf(country.id) > -1
      country.children.forEach(province => {
        province.disabled = selected_ids.indexOf(province.value) > -1
        province.children.forEach(city => city.disabled = selected_ids.indexOf(city.value) > -1)
      })
    })
    return locations_filtered
  },

  render () {
    const props = this.props
    let location_options = []
    if (this.props.locations.filtered.length > 0) {
      location_options = [
        { title: 'by Status', value: props.locations.lpd_statuses },
        { title: 'by Country', value: this.getAvailableLocations() || [] }
      ]
    }

    const locations = props.locations.raw || []
    if (props.multi) {
      return (
        <form className={props.classes}>
          <h3>Locations
            <DropdownMenu
              items={location_options}
              sendValue={this.props.selectLocation}
              item_plural_name='Locations'
              style='icon-button right'
              icon='fa-plus'
              grouped/>
          </h3>
          { props.locations.raw ? <a className='remove-filters-link' onClick={this.props.clearSelectedLocations}>Remove All </a> : '' }
          <List items={this.props.selected_locations} removeItem={this.props.deselectLocation} />
          <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Location</h3>
          <RegionTitleMenu
            locations={locations}
            selected={this.props.selected_locations[0]}
            sendValue={this.props.setLocations}
          />
        </div>
      )
    }
  }
})

export default LocationSelector
