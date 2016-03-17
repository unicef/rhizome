import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import List from 'components/molecules/list/List'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'

import LocationStore from 'stores/LocationStore'
import LocationSelectorStore from 'stores/LocationSelectorStore'
import LocationSelectorActions from 'actions/LocationSelectorActions'

const LocationSelector = React.createClass({
  mixins: [
    Reflux.connect(LocationSelectorStore, 'selected_locations'),
  ],

  propTypes: {
    locations: PropTypes.shape({
      lpd_statuses: PropTypes.array,
      filtered: PropTypes.array
    }).isRequired,
    preset_location_ids: PropTypes.array,
    classes: PropTypes.string
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

  render () {
    const props = this.props
    let location_options = []
    if (this.props.locations.filtered.length > 0) {
      location_options = [
        { title: 'by Status', value: props.locations.lpd_statuses },
        { title: 'by Country', value: props.locations.filtered || [] }
      ]
    }

    return (
      <div className={props.classes}>
        <h3>
          Locations
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
      </div>
    )
  }
})

export default LocationSelector
