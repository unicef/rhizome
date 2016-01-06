import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import DateRangePicker from 'component/DateTimePicker.jsx'
import LocationDropdownMenu from 'component/LocationDropdownMenu.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import DatabrowserTable from 'component/DatabrowserTable.jsx'
import List from 'component/list/List.jsx'

import ExplorerStore from 'stores/ExplorerStore'

import DataBrowserTableActions from 'actions/DataBrowserTableActions'
import ExplorerActions from 'actions/ExplorerActions'

let Explorer = React.createClass({
  mixins: [Reflux.connect(ExplorerStore)],

  componentWillMount: function () {
    ExplorerActions.getLocations()
    ExplorerActions.getIndicators()
  },

  refresh: function () {
    if (!this.state.couldLoad) return

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

    DataBrowserTableActions.getTableData(options, columns)
  },

  render: function () {
    let timePeriodStep = (
      <label>
        <div>Time Period</div>
        <DateRangePicker
          start={this.state.campaign.start}
          end={this.state.campaign.end}
          sendValue={ExplorerActions.updateDateRangePicker}
        />
      </label>
    )

    let locationStep = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <LocationDropdownMenu
          locations={this.state.locations}
          text='Select Location'
          sendValue={ExplorerActions.addLocations}
          style='databrowser__button' />
        <List items={this.state.locationSelected} removeItem={ExplorerActions.removeLocation} />
        <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
      </div>
    )

    let indicatorStep = (
      <div>
        <label htmlFor='indicators'>Indicators</label>
        <IndicatorDropdownMenu
          indicators={this.state.indicators}
          text='Choose Indicators'
          sendValue={ExplorerActions.addIndicators}
          style='databrowser__button' />
        <List items={this.state.indicatorSelected} removeItem={ExplorerActions.removeIndicator} />
      </div>
    )

    let loadDataStep = (
      <a role='button'
         onClick={this.refresh}
         className={this.state.couldLoad ? 'button success' : 'button success disabled'}
         style={{marginTop: '21px'}} >
        <i className='fa fa-fw fa-refresh' />&emsp;Load Data
      </a>
    )

    let loadDataTable = (
      <DatabrowserTable />
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
