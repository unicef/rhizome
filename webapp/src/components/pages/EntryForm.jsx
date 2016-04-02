import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'

import DropdownMenu from 'components/molecules/menus/DropdownMenu'
import DatabrowserTable from 'components/molecules/DatabrowserTable'
import List from 'components/molecules/list/List'

import EntryFormStore from 'stores/EntryFormStore'
import EntryFormActions from 'actions/EntryFormActions'

let EntryForm = React.createClass({
  mixins: [Reflux.connect(EntryFormStore)],

  componentWillMount: function () {
    EntryFormActions.initData()
  },

  render () {
    console.info('EntryForm: render()')
    return (
      <div className='row'>
        <form>
          <div className='medium-2 columns'>
            <br />
            <label htmlFor='forms'><h3>Form</h3></label>
            <DropdownMenu
              items={this.state.tags}
              sendValue={EntryFormActions.setForm}
              item_plural_name='Forms'
              text={this.state.selected.form.title}
              icon=''/>
            <br /><br />
            <label htmlFor='campaigns'><h3>Campaign</h3></label>
            <DropdownMenu
              items={this.state.campaigns}
              sendValue={EntryFormActions.setCampaign}
              item_plural_name='Campaign'
              text={this.state.selected.campaign.title}
              value_field='id'
              title_field='name'
              icon=''
              uniqueOnly/>
            <br /><br />
            <label htmlFor='locations'><h3>Locations</h3></label>
            <DropdownMenu
              items={this.state.filterLocations}
              sendValue={EntryFormActions.addLocations}
              item_plural_name='Locations'
              text='Select Locations'
              icon=''
              uniqueOnly/>
            <List items={this.state.locationSelected} removeItem={EntryFormActions.removeLocation} />

            <br /><br />
            <label className={this.state.couldLoad ? '' : 'disabled'}>
              <input type='checkbox' onClick={EntryFormActions.changeSelect}
                checked={this.state.includeSublocations && this.state.couldLoad}/>
              Include Sublocations
            </label>
          </div>
        </form>
        <div className='medium-10 columns'>
          <DatabrowserTable
            data={this.state.apiResponseData}
            selected_locations={this.state.locationSelected}
            selected_indicators={this.state.filteredIndicators}
            editable />
        </div>
      </div>
    )
  }
})

export default EntryForm
