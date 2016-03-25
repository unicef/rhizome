import _ from 'lodash'
import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import List from 'components/molecules/list/List'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import RegionTitleMenu from 'components/molecules/menus/RegionTitleMenu'

import LocationStore from 'stores/LocationStore'
import LocationSelectorStore from 'stores/LocationSelectorStore'
import LocationSelectorActions from 'actions/LocationSelectorActions'

const LocationSelector = React.createClass({
  mixins: [
    Reflux.connect(LocationSelectorStore, 'selected_locations'),
  ],

  propTypes: {
    locations: PropTypes.shape({
      index: PropTypes.object,
      lpd_statuses: PropTypes.array,
      filtered: PropTypes.array
    }).isRequired,
    preset_location_ids: PropTypes.array,
    classes: PropTypes.string,
    multi: PropTypes.bool
  },

  getDefaultProps() {
    return {
      preset_location_ids: null
    }
  },

  componentDidMount () {
    LocationStore.listen(locations => {
      if (this.props.preset_location_ids) {
        return LocationSelectorActions.setSelectedLocations(this.props.preset_location_ids)
      }
    })
  },

  componentWillReceiveProps(nextProps) {
    if (!_.isEmpty(nextProps.preset_location_ids) && nextProps.locations.index && _.isEmpty(this.state.selected_locations)) {
      this.setState({selected_locations: nextProps.preset_location_ids.map(id => nextProps.locations.index[id])})
    }
  },

  getAvailableLocations () {
    const selected_ids = this.state.selected_locations.map(location => location.id)
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
              sendValue={LocationSelectorActions.selectLocation}
              item_plural_name='Locations'
              style='icon-button right'
              icon='fa-plus'
              grouped/>
          </h3>
          <a className='remove-filters-link' onClick={LocationSelectorActions.clearSelectedLocations}>Remove All </a>
          <List items={this.state.selected_locations} removeItem={LocationSelectorActions.deselectLocation} />
          <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Location</h3>
          <RegionTitleMenu
            locations={locations}
            selected={this.state.selected_locations[0]}
            sendValue={LocationSelectorActions.setSelectedLocations}
          />
        </div>
      )
    }
  }
})

export default LocationSelector
