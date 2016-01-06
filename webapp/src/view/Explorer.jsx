import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'

import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import DatabrowserTable from 'component/DatabrowserTable.jsx'
import List from 'component/list/List.jsx'

import ExplorerStore from 'stores/ExplorerStore'

import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import ExplorerActions from 'actions/ExplorerActions'

let Explorer = React.createClass({
  getInitialState: function () {
    return {
      indicators: [],
      indicatorSelected: [],
      locationSelected: [],
      columns: [],
      rows: [],
      loading: true,
      options: null
    }
  },

  mixins: [Reflux.connect(ExplorerStore, 'data')],

  componentWillMount: function () {
    ExplorerActions.getLocations()
    api.indicatorsTree()
      .then(response => {
        this.setState({
          indicators: response.objects,
          indicatorMap: _.indexBy(response.flat, 'id')
        })
      })
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
    this.state.locationSelected.push(this.state.data.locationMap[id])
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

    if (this.state.data.campaign.start) {
      options.campaign_start = this.state.data.campaign.start
    }

    if (this.state.data.campaign.end) {
      options.campaign_end = this.state.data.campaign.end
    }

    this.state.indicatorSelected.forEach(indicator => {
      options.indicator__in.push(indicator.id)
      columns.push(indicator.title)
    })

    _.defaults(options, pagination, _.omit(this.state.pagination, 'total_count'))
    this.state.columns = columns
    this.state.options = options

    DataBrowserTableActions.apiCall(this.state.options, columns)
  },

  render: function () {
    let timePeriodStep = (
      <label>
        <div>Time Period</div>
        <DateRangePicker
          start={this.state.data.campaign.start}
          end={this.state.data.campaign.end}
          sendValue={ExplorerActions.updateDateRangePicker}
        />
      </label>
    )

    let locationStep = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <LocationDropdownMenu
          locations={this.state.data.locations}
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

    let loadDataTable = (
      <DatabrowserTable
        fields={this.state.columns}
        options={this.state.options} />
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
