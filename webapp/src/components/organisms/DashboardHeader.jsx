import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/atoms/AsyncButton'
import IconButton from 'components/atoms/IconButton'
import TitleInput from 'components/molecules/TitleInput'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import RegionDropdown from 'components/molecules/menus/RegionDropdown'
import DistrictDropdown from 'components/molecules/menus/DistrictDropdown'
import LocationStore from 'stores/LocationStore'

const DashboardHeader = React.createClass({

  mixins: [
    Reflux.connect(LocationStore, 'locations'),
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

  _setLocation: function (location) {
    this.props.rows.forEach(row => {
      row.charts.forEach(uuid => DashboardChartsActions.setLocations(location, uuid))
    })
  },

  _setIndicatorFilter: function (filter) {
    this.props.rows.forEach(row => {
      row.charts.forEach(uuid => DashboardChartsActions.setIndicatorFilter(filter, uuid))
    })
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
      <div className='dashboard-filters'>
        <RegionDropdown
          locations={this.state.locations.raw || []}
          selected={props.selected_locations[0]}
          sendValue={this._setLocation}
          hideLastLevel
        />
        <DistrictDropdown selected={props.indicator_filter} sendValue={this._setIndicatorFilter} />
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
      <header className='row dashboard-header'>
        <div className='medium-5 columns medium-text-left small-text-center'>
          { editMode ? title_bar : <h1>{props.title || 'Untitled Dashboard'}</h1> }
        </div>
        <div className='medium-7 columns medium-text-right small-text-center dashboard-actions'>
          { dashboard_filters }
          { save_dashboard_button }
          { edit_mode_toggle }
        </div>
      </header>
    )
  }
})

export default DashboardHeader
