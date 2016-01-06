import _ from 'lodash'
import React from 'react'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import DatabrowserTable from 'component/DatabrowserTable.jsx'
import List from 'component/list/List.jsx'

let {
  SimpleDataTable, SimpleDataTableColumn
} = require('react-datascope')

let Explorer = React.createClass({
  getInitialState: function () {
    return {
      indicators: [],
      indicatorSelected: [],
      locations: [],
      locationSelected: [],
      campaign: {
        start: '',
        end: ''
      },
      columns: [],
      rows: [],
      loading: true,
      options: null,
      data: null,
      schema: null
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

  refresh: function (pagination) {
    let locations = _.map(this.state.locationSelected, 'id')
    let options = {indicator__in: []}
    let columns = ['location', 'campaign']

    if (this.state.locationSelected.length > 0) {
      options.location__in = locations
    }

    if (this.state.campaign.start) {
      options.campaign_start = this.state.campaign.start
    }

    if (this.state.campaign.end) {
      options.campaign_end = this.state.campaign.end
    }

    this.state.indicatorSelected.forEach(indicator => {
      options.indicator__in.push(indicator.id)
      columns.push(indicator.title)
    })

    _.defaults(options, pagination, _.omit(this.state.pagination, 'total_count'))
    this.state.columns = columns
    this.state.options = options

    this.setState({
      loading: false
    })
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
        <LocationDropdownMenu
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
         onClick={this.refresh}
         v-class='disabled: !hasSelection'
         style={{marginTop: '21px'}} >
        <i className='fa fa-fw fa-refresh' />&emsp;Load Data
      </a>
    )

    let loadDataTable = this.state.loading
      ? <div className='medium-12 columns ds-data-table-empty'>No data.</div>
      : (<DatabrowserTable
            getData={api.datapoints}
            fields={this.state.columns}
            options={this.state.options} >
          <SimpleDataTable>
            {this.state.columns.map(column => {
              return <SimpleDataTableColumn name={column}/>
            })}
          </SimpleDataTable>
        </DatabrowserTable>
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
            {loadDataTable}

            <div className='medium-12 columns' style={{textAlign: 'right'}}>
              <a role='button' className='button success' aria-label='Download All'
                v-class='disabled: !hasSelection'
                v-on='click: download()'>
                <i className='fa fa-fw fa-download'></i>&emsp;Download All
              </a>
            </div>
          </div>
        </div>
        <iframe width='0' height='0' src='' className='hidden'></iframe>
      </div>
    )
  }
})

export default Explorer
