import _ from 'lodash'
import moment from 'moment'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'

import RegionTitleMenu from 'component/menus/RegionTitleMenu'
import DropdownMenu from 'component/dropdown-menus/DropdownMenu.jsx'
import CampaignDropdownMenu from 'component/dropdown-menus/CampaignDropdownMenu.jsx'
import MapFormStore from 'stores/MapFormStore'
import MapFormActions from 'actions/MapFormActions'

import Modal from 'react-modal'

var appElement = document.getElementById('main')

Modal.setAppElement(appElement)
Modal.injectCSS()

var MapForm = React.createClass({
  propTypes: {
    source_object_map_id: React.PropTypes.number.isRequired,
    onModalClose: React.PropTypes.func.isRequired
  },

  mixins: [Reflux.connect(MapFormStore, 'data')],

  componentWillMount: function () {
    MapFormActions.getLocations()
    MapFormActions.getCampaigns()
    MapFormActions.getIndicators()
  },

  getInitialState: function () {
    return {
      modalIsOpen: false,
      master_object_id: null,
      master_object_name: null,
      source_object_code: null,
      content_type: null
    }
  },

  openModal: function () {
    api.get_source_object_map({id: this.props.source_object_map_id}, null, {'cache-control': 'no-cache'})
      .then(response => {
        this.setState(
          {
            source_object_code: response.objects[0].source_object_code,
            content_type: response.objects[0].content_type,
            master_object_id: response.objects[0].master_object_id,
            modalIsOpen: true
          })
      })
  },

  closeModal: function () {
    this.props.onModalClose()
    this.setState({modalIsOpen: false, content_type: null})
  },

  postMetaMap: function (masterObjectId) {
    api.post_source_object_map({
      id: this.props.source_object_map_id,
      master_object_id: masterObjectId,
      mapped_by_id: 1 // FIXME
    }).then(response => {
      this.setState({
        master_object_id: response.objects.master_object_id,
        master_object_name: response.objects.master_object_name
      })
    })
  },

  renderDropDown: function (content_type) {
    var defaultSelected = {'name': 'please map..'}

    function loadText (message) {
      return <div className='csv-upload__loading'><i className='fa fa-spinner fa-spin' />&nbsp;Loading {message}...</div>
    }

    if (content_type === 'location') {
      if (!this.state.data.locations) {
        return loadText('Locations')
      }
      return <div><RegionTitleMenu
        locations={this.state.data.locations}
        selected={defaultSelected}
        sendValue={this.postMetaMap}/></div>
    }
    if (content_type === 'indicator') {
      if (!this.state.data.indicators) {
        return loadText('Indicators')
      }
      return <DropdownMenu
          items={this.state.data.indicators}
          sendValue={this.postMetaMap}
          item_plural_name='Indicators'
          text='Map Indicator'/>
    }
    if (content_type === 'campaign') {
      if (!this.state.data.campaigns) {
        return loadText('Campaigns')
      }
      var office = {
        1: 'Nigeria',
        2: 'Afghanistan',
        3: 'Pakistan'
      }
      var campaigns = this.state.data.campaigns.map(campaign => {
        return _.assign({}, campaign, {
          slug: office[campaign.office_id] + ' ' + moment(campaign.start_date).format('MMM YYYY')
        })
      })

      campaigns.reverse()
      return <div>
        <CampaignDropdownMenu
          text={defaultSelected}
          campaigns={campaigns}
          sendValue={this.postMetaMap} />
      </div>
    }
  },

  render: function () {
    var sourceObjectMapId = this.props.source_object_map_id
    var modalStyle = {width: 400, height: 300, marginLeft: 400}
    return <div>
      <button className='tiny' onClick={this.openModal}> map!</button>
      <Modal
        style={modalStyle}
        isOpen={this.state.modalIsOpen}
        onRequestClose={this.closeModal}>
        <h1> Source Map Id: {sourceObjectMapId} </h1>
        <form>
          <h2> Content Type: {this.state.content_type} </h2>
          <h2> Source Code: {this.state.source_object_code} </h2>
          <h2> Master Object ID: {this.state.master_object_id} </h2>
          {this.renderDropDown(this.state.content_type)}
        </form>
      </Modal></div>
  }
})

export default MapForm
