import React, { PropTypes } from 'react'
import Reflux from 'reflux'
import List from 'components/molecules/list/List'
import DropdownMenu from 'components/molecules/menus/DropdownMenu'


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
    onChange: PropTypes.func.isRequired,
    classes: PropTypes.string
  },

  componentDidMount () {
    LocationSelectorActions.setSelectedLocations(1)
  },

  componentDidUpdate(prevProps, prevState) {
    this.props.onChange(this.state.selected_locations)
  },

  render () {
    const props = this.props
    const location_options = [
      { title: 'by Status', value: props.locations.lpd_statuses },
      { title: 'by Country', value: props.locations.filtered || [] }
    ]

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
