import _ from 'lodash'
import React from 'react'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationsDropDownMenu from 'component/LocationDropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import List from 'component/list/List.jsx'

var Explorer = React.createClass({
  getInitialState: function () {
    return {
      indicators: [],
      indicatorSelected: [],
      locations: [],
      locationSelected: [],
      campaign: {
        start: '',
        end: ''
      }
    }
  },

  componentWillMount: function () {
    api.indicatorsTree()
      .then(response => {
        this.setState({
          indicators: response.objects,
          indicatorMap: _.indexBy(response.flat, 'id')
        })
      })
    api.locations()
      .then(response => {
        this.setState({
          locations: _(response.objects)
            .map(location => {
              return {
                'title': location.name,
                'value': location.id,
                'parent': location.parent_location_id
              }
            })
            .sortBy('title')
            .reverse()
            .thru(_.curryRight(treeify)('value'))
            .map(ancestryString)
            .value(),
          locationMap: _.indexBy(response.objects, 'id')
        })
      })
  },

  updateDateRangePicker: function (key, value) {
    this.state.campaign[key] = value
  },

  addIndicators: function (id) {
    this.state.indicatorSelected.push(this.state.indicatorMap[id])
    this.forceUpdate()
  },

  removeIndicatored: function (id) {
    _.remove(this.state.indicatorSelected, {id: id})
    this.forceUpdate()
  },

  addLocations: function (id) {
    this.state.locationSelected.push(this.state.locationMap[id])
    this.forceUpdate()
  },

  removeLocation: function (id) {
    _.remove(this.state.locationSelected, {id: id})
    this.forceUpdate()
  },

  render: function () {
    let timePeriodStep = (
      <label>
        <div>Time Period</div>
        <DateRangePicker
          start={this.state.campaign.start}
          end={this.state.campaign.end}
          sendValue={this.updateDateRangePicker}
        />
      </label>
    )

    let locationStep = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <LocationsDropDownMenu
          locations={this.state.locations}
          text='Select Location'
          sendValue={this.addLocations}
          style='databrowser__button' />
        <List items={this.state.locationSelected} removeItem={this.removeLocation} />
        <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
      </div>
    )

    let indicatorStep = (
      <div>
        <label htmlFor='indicators'>Indicators</label>
        <IndicatorDropdownMenu
          indicators={this.state.indicators}
          text='Choose Indicators'
          sendValue={this.addIndicators}
          style='databrowser__button' />
        <List items={this.state.indicatorSelected} removeItem={this.removeIndicatored} />
      </div>
    )

    let loadDataStep = (
      <a className='button success'
         role='button'
         v-on='click : refresh({ offset: 0 })'
         v-class='disabled: !hasSelection'
         style={{marginTop: '21px'}} >
        <i className='fa fa-fw fa-refresh'
           v-class='fa-spin : table.loading'></i>&emsp;Load Data
      </a>
    )

    return (
      <div>
        <div className='row'>
          <div className='small-12 columns'>
            <h1 style={{textAlign: 'left'}}>Raw Data</h1>
          </div>
        </div>

        <div className='row'>
          <div className='medium-3 columns'>
            <from className='inline'>
              {timePeriodStep}
              {locationStep}
              {indicatorStep}
              {loadDataStep}
            </from>
          </div>

          <div className='medium-9 columns'>
            <vue-table v-with='table'></vue-table>

            <div className='medium-6 columns'
              v-component='vue-pagination'
              v-with='offset: pagination.offset,
                      limit: pagination.limit,
                      total_count: pagination.total_count'></div>

            <div className='medium-4 columns' style={{textAlign: 'right'}}>
              <a role='button' className='button success' aria-label='Download All'
                v-class='disabled: !hasSelection'
                v-on='click: download()'>
                <i className='fa fa-fw fa-download'></i>&emsp;Download All
              </a>
            </div>
          </div>
        </div>
        <iframe width='0' height='0' src='{{ src }}' className='hidden'></iframe>
      </div>
    )
  }
})

export default Explorer
