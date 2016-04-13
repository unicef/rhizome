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
    let sourceSelector = ''
    // let sourceSelector = (<br/><br/>
    //   <label htmlFor='source'><h3>Source</h3></label>
    //   <DropdownMenu
    //     items={this.state.sourceList}
    //     sendValue={EntryFormActions.setSource}
    //     value_field='id'
    //     item_plural_name='Source'
    //     text={this.state.selected.source.title}
    //     icon=''
    //     uniqueOnly/>)

    return (
      <div className='row'>
        <form>
          <div className='medium-2 columns'>
            <br />
            <label htmlFor='forms'><h3>Form</h3></label>
            <DropdownMenu
              items={this.state.tags}
              sendValue={EntryFormActions.setForm}
              value_field='id'
              title_field='name'
              item_plural_name='Form'
              text={this.state.selected.form.title}
              icon=''
              uniqueOnly/>
              {sourceSelector}
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
