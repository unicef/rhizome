import _ from 'lodash'
import moment from 'moment'
import React, { Component, PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/global/Placeholder'
import RadioGroup from 'components/form/RadioGroup'
import DateRangeSelect from 'components/select/DateRangeSelect'
import DateTimePicker from 'react-widgets/lib/DateTimePicker'
import DropdownButton from 'components/button/DropdownButton'
import DropdownList from 'react-widgets/lib/DropdownList'
import IconButton from 'components/button/IconButton'
import Multiselect from 'react-widgets/lib/Multiselect'

class LocationDetail extends Component {

  constructor (props) {
    super(props)
    this.state = {}
  }

  componentDidMount() {
    if (!this.props.location_types.raw) {
      this.props.getAllLocationTypes()
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.location.id !== this.state.id) {
      const location = Object.assign({}, nextProps.location)
      delete location.created_at
      this.setState(location)
    }
  }

  _updateParam = (param, value) => {
    const location = {}
    location[param] = value
    this.setState(location)
  }

  _saveLocation = event => {
    event.preventDefault()
    this.props.updateLocation(this.state)
  }

  render = () => {
    if (!this.state.id) {
      return <Placeholder height={300} />
    }

    const selected_location = this.state.parent_location_id ? this.props.locations.index[this.state.parent_location_id] : {name: 'Select Location'}
    const selected_location_type = this.state.location_type_id ? this.props.location_types.index[this.state.location_type_id] : {name: 'Select Location Type'}
    return (
      <form className='medium-6 medium-centered columns resource-form' onSubmit={this._saveLocation}>
        <h2>Location ID: {this.state.id}</h2>
        <label>Type:
          <DropdownButton
            style='full-width'
            items={this.props.location_types.raw || []}
            title_field='name'
            value_field='id'
            sendValue={id => this._updateParam('location_type_id', id)}
            text={selected_location_type.name}
          />
        </label>
        {
          selected_location_type.name !== 'Country' ? (
            <label>Parent Location:
              <DropdownButton
                style='full-width'
                items={this.props.locations.list || []}
                sendValue={id => this._updateParam('parent_location_id', id)}
                text={selected_location.name}
              />
            </label>
          ) : null
        }
        <label htmlFor='name'>Name:
          <input type='text' defaultValue={this.state.name}
            onBlur={event => this._updateParam('name', event.target.value)}
          />
        </label>
        <label htmlFor='location_code'>Location Code:
          <input type='text' defaultValue={this.state.location_code}
            onBlur={event => this._updateParam('location_code', event.target.value)}
          />
        </label>
        <div className='row'>
          <label className='medium-6 columns'>Latitude:
            <input type='text' defaultValue={this.state.latitude}
              onBlur={event => this._updateParam('latitude', event.target.value)}
            />
          </label>
          <label className='medium-6 columns'>Longitude:
            <input type='text' defaultValue={this.state.longitude}
              onBlur={event => this._updateParam('longitude', event.target.value)}
            />
          </label>
        </div>
        <label>LPD Status:
          <RadioGroup
            name={'lpd_status'}
            value={this.state.lpd_status || 0}
            onChange={id => this._updateParam('lpd_status', parseInt(id))}
            horizontal
            prefix='lpd_status'
            values={[
              {value: 0, title: 'None'},
              {value: 1, title: '1'},
              {value: 2, title: '2'},
              {value: 3, title: '3'}
            ]}
          />
        </label>
        <button className='large primary button expand'>Save</button>
      </form>
    )
  }
}

export default LocationDetail
