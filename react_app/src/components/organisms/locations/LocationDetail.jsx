import _ from 'lodash'
import moment from 'moment'
import React, { Component, PropTypes } from 'react'
import {AgGridReact} from 'ag-grid-react';
import Placeholder from 'components/global/Placeholder'
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

  _addLocationTag = id => {
    const tag_array = JSON.parse(this.state.tag_json)
    tag_array.push(parseInt(id))
    this._updateParam('tag_json', JSON.stringify(tag_array))
  }

  _removeLocationTag = (event, tag_id) => {
    event.preventDefault()
    const tag_array = JSON.parse(this.state.tag_json)
    const index = tag_array.indexOf(tag_id)
    tag_array.splice(index, 1)
    this._updateParam('tag_json', JSON.stringify(tag_array))
  }

  render = () => {
    if (!this.state.id) {
      return <Placeholder height={300} />
    }

    const selected_location_tag = this.state.top_lvl_location_tag_id ? this.props.locations.tag_index[this.state.top_lvl_location_tag_id] : {tag_name: 'Add Tag'}
    const tag_array = JSON.parse(this.state.tag_json)
    const all_tags = _.toArray(this.props.locations.tag_index)
    const filtered_tags = all_tags.filter(tag => tag_array.indexOf(tag.id) === -1)
    const location_tag_select = (
      <div>
        <h3 style={{marginBottom: '.1rem'}}>Tags:
          <DropdownButton
            items={filtered_tags}
            sendValue={this._addLocationTag}
            title_field='tag_name'
            value_field='id'
            item_plural_name='Locations'
            style='icon-button button right pad-right'
            icon='fa-plus'
            searchable
          />
        </h3>
        <ul className='multi-select-list'>
          {tag_array.map(tag_id => (
            <li key={tag_id}>
              <IconButton className='clear-btn' icon='fa-times-circle' onClick={e => this._removeLocationTag(e, tag_id)} />
              { this.props.locations.tag_index[tag_id].tag_name }
            </li>
          ))}
        </ul>
      </div>
    )

    const data_formats = [
      {title: 'Percent', value: 'pct'},
      {title: 'Integer', value: 'int'},
      {title: 'True/False', value: 'bool'},
      {title: 'Date', value: 'date'},
    ]
    const data_format_index = _.keyBy(data_formats, 'value')
    const selected_data_format = data_format_index[this.state.data_format].title
    const showBounds = this.state.data_format !== 'bool' && this.state.data_format !== 'date'
    return (
      <form className='medium-8 medium-centered columns resource-form' onSubmit={this._saveLocation}>
        <div className='medium-7 columns'>
          <h2>Location ID: {this.state.id}</h2>
          <label htmlFor='name'>Name:
            <input type='text' defaultValue={this.state.name}
              onBlur={event => this._updateParam('name', event.target.value)}
            />
          </label>
          <label htmlFor='short_name'>Short Name:
            <input type='text' defaultValue={this.state.short_name}
              onBlur={event => this._updateParam('short_name', event.target.value)}
            />
          </label>
          <label htmlFor='source_name'>Source Name:
            <input type='text' defaultValue={this.state.source_name}
              onBlur={e => this._updateParam('source_name', e.target.value)}
            />
          </label>
          <label htmlFor='description'>Description:
            <textarea defaultValue={this.state.description}
              onBlur={e => this._updateParam('description', e.target.value)}
            />
          </label>
          <label>Data Format:
            <DropdownButton
              style='full-width'
              items={data_formats}
              sendValue={format => this._updateParam('data_format', format)}
              text={selected_data_format}
            />
          </label>
          {
            showBounds ? (
            <div className='row'>
              <label className='medium-6 columns'>Good Bound:
                <input type='text' defaultValue={this.state.good_bound}
                  onBlur={event => this._updateParam('good_bound', event.target.value)}
                />
              </label>
              <label className='medium-6 columns'>Bad Bound:
                <input type='text' defaultValue={this.state.bad_bound}
                  onBlur={event => this._updateParam('bad_bound', event.target.value)}
                />
              </label>
            </div>
            ) : null
          }
          <button className='large primary button expand'>Save</button>
        </div>
        <div className='medium-5 columns'>
          <br />
          {location_tag_select}
        </div>
      </form>
    )
  }
}

export default LocationDetail
