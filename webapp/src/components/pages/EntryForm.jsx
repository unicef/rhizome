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
    let formIdSelected = this.state.formIdSelected
    let formName = 'Select Form'
    let indicatorSelected = []
    if (formIdSelected) {
      let formDef = _.find(this.state.entryFormDefinitions,
        function (d) { return d.form_id.toString() === formIdSelected })
      formName = formDef.title
      formDef.indicator_id_list.forEach(indicator_id => {
        indicatorSelected.push(this.state.indicatorMap[indicator_id])
      })
    }

    let campaignIdSelected = this.state.campaignIdSelected
    let campaignName = 'Select Campaign'
    let campaignObj = null;
    if (campaignIdSelected) {
      campaignObj = _.find(this.state.campaigns,
        function (c) { return c.id.toString() === campaignIdSelected })
    }

    if (campaignObj) {
      campaignName = campaignObj.name
    }

    return (
      <div className='row'>
        <form>
          <div className='medium-2 columns'>
            <br />
            <label htmlFor='forms'><h3>Form</h3></label>
            <DropdownMenu
              items={this.state.entryFormDefinitions}
              sendValue={EntryFormActions.setForm}
              item_plural_name='Forms'
              text={formName}
              icon=''/>
            <br /><br />
            <label htmlFor='campaigns'><h3>Campaign</h3></label>
            <DropdownMenu
              items={this.state.campaigns}
              sendValue={EntryFormActions.setCampaign}
              item_plural_name='Campaign'
              text={campaignName}
              title_field='name'
              value_field='id'
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
            selected_indicators={indicatorSelected}
            editable />
        </div>
      </div>
    )
  }
})

export default EntryForm
