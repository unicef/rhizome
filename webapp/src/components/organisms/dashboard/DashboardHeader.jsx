import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/button/AsyncButton'
import IconButton from 'components/button/IconButton'
import TitleInput from 'components/TitleInput'
import DashboardContainerActions from 'actions/DashboardContainerActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import CampaignSelect from 'components/select/CampaignSelect'
import LocationSelect from 'components/select/LocationSelect'
import DistrictSelect from 'components/select/DistrictSelect'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import RootStore from 'stores/RootStore'

const DashboardHeader = React.createClass({

  mixins: [
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connectFilter(RootStore, 'superuser', store => store.superuser)
  ],

  propTypes: {
    dashboard_id: PropTypes.number,
    title: PropTypes.string,
    editMode: PropTypes.bool
  },

  getInitialState: function () {
    return {
      titleEditMode: false
    }
  },

  _toggleTitleEdit: function (title) {
    if (_.isString(title)) {
      DashboardContainerActions.setDashboardTitle(title)
    }
    this.setState({titleEditMode: !this.state.titleEditMode})
  },

  render () {
    const props = this.props
    const editMode = props.editMode
    const title_bar = this.state.titleEditMode ? (
      <TitleInput initialText={props.title} save={this._toggleTitleEdit}/>
    ) : (
      <h1 onClick={this._toggleTitleEdit}>
        <a>{props.title || 'Untitled Dashboard'}</a>
      </h1>
    )

    const save_dashboard_button = editMode ? (
      <AsyncButton
        text='Save Dashboard'
        alt_text='Saving ...'
        isBusy={props.saving}
        onClick={() => DashboardContainerActions.saveDashboard(props.dashboard_id)}
      />
    ) : null

    const dashboard_filters = (
      <div className='page-header-filters'>
        <CampaignSelect
          campaigns={this.state.campaigns.raw || []}
          selected={props.selected_campaigns[0]}
          sendValue={DashboardContainerActions.setCampaign}
        />
        <LocationSelect
          locations={this.state.locations.raw || []}
          selected={props.selected_locations[0]}
          sendValue={DashboardContainerActions.setLocation}
          hideLastLevel
        />
        <DistrictSelect selected={props.indicator_filter} sendValue={DashboardContainerActions.setIndicatorFilter} />
      </div>
    )

    const edit_mode_toggle =  editMode ? (
      <IconButton onClick={DashboardContainerActions.toggleEditMode} icon='fa-times' />
    ) : (
      <button className='button' onClick={DashboardContainerActions.toggleEditMode}>
        Edit
      </button>
    )

    return (
      <header className='row page-header'>
        <div className='medium-5 columns medium-text-left small-text-center'>
          { editMode ? title_bar : <h1>{props.title || 'Untitled Dashboard'}</h1> }
        </div>
        <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
          { dashboard_filters }
          { save_dashboard_button }
          { this.state.superuser ? edit_mode_toggle : null}
        </div>
      </header>
    )
  }
})

export default DashboardHeader
