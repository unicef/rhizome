import _ from 'lodash'
import React from 'react'
import api from 'data/api'

import ancestryString from 'data/transform/ancestryString'
import treeify from 'data/transform/treeify'

import DropdownMenu from 'component/DropdownMenu.jsx'
import MenuItem from 'component/MenuItem.jsx'

import DateRangePicker from 'component/DateTimePicker.jsx'
import IndicatorDropdownMenu from 'component/IndicatorDropdownMenu.jsx'
import List from 'component/list/List.jsx'

function filterMenu (items, pattern) {
  if (!pattern || pattern.length < 3) {
    return items
  }

  let match = _.partial(findMatches, _, new RegExp(pattern, 'gi'))

  return _(items).map(match).flatten().value()
}

function findMatches (item, re) {
  let matches = []

  if (re.test(_.get(item, 'title'))) {
    matches.push(_.assign({}, item, {filtered: true}))
  }

  if (!_.isEmpty(_.get(item, 'children'))) {
    _.each(item.children, function (child) {
      matches = matches.concat(findMatches(child, re))
    })
  }

  return matches
}

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
      },
      locationSearch: ''
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

  addLocations (id) {
    this.state.locationSelected.push(this.state.locationMap[id])
    this.forceUpdate()
  },

  removeLocation (id) {
    _.remove(this.state.locationSelected, {id: id})
    this.forceUpdate()
  },

  setLocationSearch (pattern) {
    this.setState({
      locationSearch: pattern
    })
  },

  render: function () {
    let timePeriodSetp = (
      <label>
        <div>Time Period</div>
        <DateRangePicker
          start={this.state.campaign.start}
          end={this.state.campaign.end}
          sendValue={this.updateDateRangePicker}
        />
      </label>
    )

    let locations = MenuItem.fromArray(filterMenu(this.state.locations, this.locationSearch), this.addLocations)
    let locationSetp = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <DropdownMenu
          icon='fa-globe'
          text='Select Location'
          style='databrowser__button'
          searchable
          onSearch={this.setLocationSearch}>
          {locations}
        </DropdownMenu>
        <List items={this.state.locationSelected} removeItem={this.removeLocation} />
        <div id='locations' placeholder='0 selected' multi='true' searchable='true' className='search-button'></div>
      </div>
    )

    let indicatorSetp = (
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
              {timePeriodSetp}
              {locationSetp}
              {indicatorSetp}
              <div>
                <a className='button success' role='button' v-on='click : refresh({ offset: 0 })' v-class='disabled: !hasSelection' style={{marginTop: '21px'}}>
                  <i className='fa fa-fw fa-refresh' v-class='fa-spin : table.loading'></i>&emsp;Load Data
                </a>
              </div>
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
