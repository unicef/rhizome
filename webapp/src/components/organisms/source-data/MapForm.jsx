import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import api from 'data/api'

import LocationSelect from 'components/atoms/select/LocationSelect'
import DropdownButton from 'components/atoms/button/DropdownButton'
import CampaignStore from 'stores/CampaignStore'
import LocationStore from 'stores/LocationStore'
import IndicatorStore from 'stores/IndicatorStore'

import Modal from 'react-modal'

var appElement = document.getElementById('main')

Modal.setAppElement(appElement)
Modal.injectCSS()

var MapForm = React.createClass({
  propTypes: {
    source_object_map_id: React.PropTypes.number.isRequired,
    onModalClose: React.PropTypes.func.isRequired
  },

  mixins: [
    Reflux.connect(CampaignStore, 'campaigns'),
    Reflux.connect(LocationStore, 'locations'),
    Reflux.connect(IndicatorStore, 'indicators')
  ],

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
      if (!this.state.locations.index) {
        return loadText('Locations')
      }
      return <div><LocationSelect
        locations={_.toArray(this.state.locations.index)}
        selected={defaultSelected}
        sendValue={this.postMetaMap}/></div>
    }
    if (content_type === 'indicator') {
      if (!this.state.indicators.list) {
        return loadText('Indicators')
      }
      return <DropdownButton
          items={this.state.indicators.list}
          sendValue={this.postMetaMap}
          item_plural_name='Indicators'
          text='Map Indicator'/>
    }
    if (content_type === 'campaign') {
      if (!this.state.campaigns.list) {
        return loadText('Campaigns')
      }

      return <DropdownButton
          items={this.state.campaigns.list}
          value_field='id'
          title_field='name'
          sendValue={this.postMetaMap}
          item_plural_name='Campaigns'
          text='Map Campaign'/>
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
