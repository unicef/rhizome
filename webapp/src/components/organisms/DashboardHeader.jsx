import _ from 'lodash'
import React, {PropTypes} from 'react'
import Reflux from 'reflux'

import AsyncButton from 'components/atoms/AsyncButton'
import TitleInput from 'components/molecules/TitleInput'
import DashboardPageActions from 'actions/DashboardPageActions'
import DashboardChartsActions from 'actions/DashboardChartsActions'
import RegionTitleMenu from 'components/molecules/menus/RegionTitleMenu'
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
        <RegionTitleMenu
          locations={this.state.locations.raw || []}
          selected={props.selected_locations[0]}
          sendValue={this._setLocation}
          hideLastLevel
        />
      </div>
    )

    return (
      <header className='row dashboard-header'>
        <div className='medium-6 columns medium-text-left small-text-center'>
          { editMode ? title_bar : <h1>{props.title || 'Untitled Dashboard'}</h1> }
        </div>
        <div className='medium-6 columns medium-text-right small-text-center'>
          { dashboard_filters }
          { save_dashboard_button }
          <button className='button' onClick={DashboardPageActions.toggleEditMode}>
            { !editMode ? 'Edit' : 'Exit Edit Mode' }
          </button>
        </div>
      </header>
    )
  }
})

export default DashboardHeader
