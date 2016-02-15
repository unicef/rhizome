import React from 'react'
import Reflux from 'reflux'

import DropdownMenu from '02-molecules/menus/DropdownMenu'
import TableEditale from '02-molecules/TableEditable'
import List from '02-molecules/list/List'

import EntryFormStore from 'stores/EntryFormStore'
import EntryFormActions from 'actions/EntryFormActions'

let EntryForm = React.createClass({
  mixins: [Reflux.connect(EntryFormStore)],

  componentWillMount: function () {
    EntryFormActions.initData()
  },

  _setForm: function (event) {
    EntryFormActions.setForm(event.target.value)
  },

  _setCampaign: function (event) {
    EntryFormActions.setCampaign(event.target.value)
  },

  refresh: function () {
    if (!this.state.couldLoad) return
    EntryFormActions.getTableData()
  },

  render () {
    let formName = this.state.formSelected ? this.state.formSelected.form_name : 'Select a Form'
    let formDropDown = (
      <div>
        <label htmlFor='forms'>Forms</label>
        <DropdownMenu
          items={this.state.entryFormDefinitions}
          sendValue={EntryFormActions.setForm}
          item_plural_name='Forms'
          text={formName}
          title_field='form_name'
          value_field='form_id'
          uniqueOnly/>
      </div>
    )
    let campaignDropdown = (
      <div>
        <label htmlFor='campaigns'>Campaigns</label>
        <DropdownMenu
          items={this.state.campaigns}
          sendValue={this._setCampaign}
          item_plural_name='Campaign'
          text={this.state.campaignSelected}
          title_field='name'
          icon='fa-globe'
          uniqueOnly/>
      </div>
    )

    let locationDropDown = (
      <div>
        <label htmlFor='locations'>Locations</label>
        <DropdownMenu
          items={this.state.filterLocations}
          sendValue={EntryFormActions.addLocations}
          item_plural_name='Locations'
          text='Select Location'
          icon='fa-globe'
          uniqueOnly/>
        <List items={this.state.locationSelected} removeItem={EntryFormActions.removeLocation} />
      </div>
    )

    let includeSublocations = (
      <div>
        <br />
        <label className={this.state.couldLoad ? '' : 'disabled'}>
          <input type='checkbox'
            checked={this.state.includeSublocations && this.state.couldLoad}
            onClick={EntryFormActions.changeSelect} />Include Sublocations
        </label>
      </div>
    )

    let loadEntryForm = (
      <div>
        <br />
        <a role='button'
          onClick={this.refresh}
          className={this.state.couldLoad ? 'button success' : 'button success disabled'} >
          <i className='fa fa-fw fa-refresh' />Load Entry Form
        </a>
      </div>
    )

    return (
      <div className='row'>
        <form>
          <div className='medium-2 columns'>
            {formDropDown}
            {campaignDropdown}
            {locationDropDown}
            {includeSublocations}
            {loadEntryForm}
          </div>
        </form>
        <div className='medium-10 columns'>
          <TableEditale data={this.state.data}
            loaded={this.state.loaded}
            indicatorSet={this.state.indicatorSet}
            indicatorMap={this.state.indicatorMap}
            locationMap={this.state.locationMap}
            locations={this.state.locations}
            campaignId={this.state.campaignSelected}/>
        </div>
      </div>
    )
  }
})

export default EntryForm
