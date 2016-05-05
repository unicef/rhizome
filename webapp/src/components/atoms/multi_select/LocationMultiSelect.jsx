import _ from 'lodash'
import React, {Component, PropTypes} from 'react'
import Reflux from 'reflux'
import List from 'components/molecules/list/List'
import DropdownButton from 'components/atoms/button/DropdownButton'
import LocationSelect from 'components/atoms/select/LocationSelect'

class LocationMultiSelect extends Component {

  static propTypes = {
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
    multi: PropTypes.bool,
    hideLastLevel: React.PropTypes.bool // Don't show any locations if they have no sub locations themselves
  }

  static defaultProps = {
    selected_locations: []
  }

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
  }

  render () {
    const props = this.props
    const locations = props.locations.raw || []
    if (props.multi) {
      return (
        <form className={props.classes}>
          <h3 style={{marginBottom: '.1rem'}}>Locations
            <DropdownButton
              items={this.getAvailableLocations() || []}
              sendValue={this.props.selectLocation}
              item_plural_name='Locations'
              style='icon-button right pad-right'
              icon='fa-plus'
            />
          </h3>
          <List items={this.props.selected_locations} removeItem={this.props.deselectLocation} />
          { props.selected_locations.length > 1 ? <a className='remove-filters-link' onClick={this.props.clearSelectedLocations}>Remove All </a> : '' }
          <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
          <br/>
        </form>
      )
    } else {
      return (
        <div className={props.classes}>
          <h3>Location</h3>
          <LocationSelect
            locations={locations}
            selected={this.props.selected_locations[0]}
            sendValue={this.props.setLocations}
            hideLastLevel={this.props.hideLastLevel}
          />
          <br/>
        </div>
      )
    }
  }
}

export default LocationMultiSelect
