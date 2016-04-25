import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/atoms/AsyncButton'
import IconButton from 'components/atoms/IconButton'
import TitleInput from 'components/molecules/TitleInput'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import CampaignDropdown from 'components/molecules/menus/CampaignDropdown'
import LocationDropdown from 'components/molecules/menus/LocationDropdown'
import DistrictDropdown from 'components/molecules/menus/DistrictDropdown'
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
      DashboardPageActions.setDashboardTitle(title)
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
        onClick={() => DashboardPageActions.saveDashboard(props.dashboard_id)}
      />
    ) : null

    const dashboard_filters = (
      <div className='page-header-filters'>
        <CampaignDropdown
          campaigns={this.state.campaigns.raw || []}
          selected={props.selected_campaigns[0]}
          sendValue={DashboardPageActions.setCampaign}
        />
        <LocationDropdown
          locations={this.state.locations.raw || []}
          selected={props.selected_locations[0]}
          sendValue={DashboardPageActions.setLocation}
          hideLastLevel
        />
        <DistrictDropdown selected={props.indicator_filter} sendValue={DashboardPageActions.setIndicatorFilter} />
      </div>
    )

    const edit_mode_toggle =  editMode ? (
      <IconButton onClick={DashboardPageActions.toggleEditMode} icon='fa-times' />
    ) : (
      <button className='button' onClick={DashboardPageActions.toggleEditMode}>
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
