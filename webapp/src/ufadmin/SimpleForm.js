import api from 'data/api'
import React from 'react'
import page from 'page'
import Reflux from 'reflux'
import ReactJson from 'react-json'

import SimpleFormStore from 'stores/SimpleFormStore'
import SimpleFormActions from 'actions/SimpleFormActions'
import SimpleFormComponent from './SimpleFormComponent'
import IndicatorTagDropdownMenu from 'component/IndicatorTagDropdownMenu.jsx'

var SimpleForm = React.createClass({
  propTypes: {
    params: React.PropTypes.object
  },

  mixins: [
    Reflux.connect(SimpleFormStore, 'store')
  ],

  contextTypes: {
    router: React.PropTypes.func
  },

  getInitialState: function () {
    return {
      objectId: null,
      extraFormData: {},
      tagTree: []
    }
  },

  componentWillMount: function () {
    var self = this
    this.setState({'objectId': this.props.params.id})
    SimpleFormActions.initialize(this.props.params.id, this.props.params.contentType)

    // Hack alert.. FIXME ( this is for the parent_tag_dropdown) //
    if (this.props.params.contentType === 'indicator_tag') {
      api.tagTree({}, null, {'cache-control': 'no-cache'}).then(function (response) {
        self.setState({'tagTree': response.objects})
      })
    }
  },

  componentWillReceiveProps: function (nextProps) {
    SimpleFormActions.initialize(nextProps.params.id, nextProps.params.contentType)
  },

  addTagToIndicator: function (tag_id) {
    var mainID = this.props.params.id
    if (mainID === null) return
    SimpleFormActions.addTagToIndicator(mainID, tag_id)
  },

  addCalculationToIndicator: function (typeInfo, indicator_id) {
    var mainID = this.props.params.id
    if (mainID === null) return

    SimpleFormActions.addCalculationToIndicator(mainID, indicator_id, typeInfo)
  },

  removeCalculationFromIndicator: function (id) {
    var mainID = this.props.params.id
    if (mainID === null) return

    SimpleFormActions.removeCalculationFromIndicator(mainID, id)
  },

  removeTagFromIndicator: function (id) {
    var mainID = this.props.params.id
    if (mainID === null) return
    SimpleFormActions.removeTagFromIndicator(mainID, id)
  },

  componentWillUpdate: function (nextProps, nextState) {
    if (nextProps.params !== this.props.params) {
      return
    }
    if (nextState.store.dataObject !== this.state.store.dataObject) {
      return
    }
    if (nextState.extraFormData !== this.state.extraFormData) {
      return
    }
  },
  onSubmit: function (e) {
    e.preventDefault()
    var data = this.refs.form_data.getValue()

    // if there is any data in the react-json form add it here //
    for (var key in this.state.extraFormData) {
      data[key] = this.state.extraFormData[key]
    }

    SimpleFormActions.baseFormSave(this.props.params.id, this.props.params.contentType, data)
  },

  setParentTag: function (e) {
    var extraFormData = {'parent_tag_id': e}
    this.setState({'extraFormData': extraFormData})
  },

  render: function () {
    var objectId = this.state.objectId
    var contentType = this.props.params.contentType
    var dataObject = this.state.store.dataObject
    var formSettings = this.state.store.formSettings
    var formData = this.state.store.formData
    if (formData && formData.hasOwnProperty('description')) {
      let description = formData.description
      delete formData.description
      formData.description = description
    }

    // TODO -> pull this from the DB

    if (objectId && !dataObject) {
      if (this.state.store.loading) {
        return <div>Loading MetaData Manager</div>
      } else {
        page('/manage_system/' + contentType + '/')
        return (
          <div>Error. There is no data received.</div>
        )
      }
    }

    if (dataObject) {
      // match up the data from the dataObject
      for (var key in formData) {
        if (dataObject.hasOwnProperty(key)) {
          formData[key] = dataObject[key]
        }
      }
    }

    var additionalFormComponents = ''
    if (contentType === 'indicator_tag' && dataObject) {
      var selected = this.state.extraFormData['parent_tag_id'] || dataObject.parent_tag_id || 'No Parent'
      var tagTree = this.state.tagTree

      additionalFormComponents = (
        <div>
          <p>{`Parent Tag: ${selected}`}</p>
          <br />
          <IndicatorTagDropdownMenu
            tag_tree={tagTree}
            text='Parent tag'
            sendValue={ this.setParentTag } />
        </div>
      )
    } else if (contentType === 'indicator') {
      additionalFormComponents = ''
    }

    var idInfo = ''
    if (this.state.store.objectId !== -1) {
      idInfo = (
        <div>
          <h5>id: {this.state.store.objectId}</h5>
          <br />
        </div>
      )
    }

    var baseFormSuccess = ''
    if (this.state.store.saveSuccess) {
      baseFormSuccess = <i className='fa fa-check'> Saved successfully </i>

      var newId = this.state.store.objectId
      this.state.store.saveSuccess = false

      if (this.props.params && this.props.params.id) {
        page('/manage_system/' + (contentType === 'indicator_tag' ? 'tags' : 'indicators'))
      } else {
        page('/manage_system/manage/' + contentType + '/' + newId)
      }

      SimpleFormActions.initialize(newId, contentType)
    }

    let subFormList = ''

    if (contentType === 'indicator') {
      subFormList = (
        <div>
          <div className='ufadmin-create-button'>
            <a className='button' href='/manage_system/manage/indicator/'>Create Indicator</a>
          </div>
          <SimpleFormComponent
            objectId={objectId}
            contentType={'indicator_tag'}
            componentTitle='Add Tags to Indicators'
            onClick={this.addTagToIndicator}
            smallItemCouldClick
            onSmallItemClick={this.removeTagFromIndicator} />
          <br />
          <SimpleFormComponent
            objectId={objectId}
            contentType='indicator_calc'
            componentTitle='Add Calculations to Indicators'
            onClick={this.addCalculationToIndicator}
            smallItemCouldClick
            onSmallItemClick={this.removeCalculationFromIndicator}
            smallIDCouldClick
            smallIDBaseUrl='/manage_system/manage/indicator/' />
        </div>
      )
    }

    return (
      <div className='row'>
        <div className='small-8 columns'>
          <div>
            <h2>Manage Admin Page</h2>
            {idInfo}
            <ReactJson value={formData} settings={formSettings} ref='form_data'/>
            {additionalFormComponents}
            <br />
            <button className='tiny' style={{ textAlign: 'right' }} onClick={ this.onSubmit }>Save</button>
          </div>
          <div>{baseFormSuccess}</div>
        </div>
        <div className='small-4 columns'>
          {subFormList}
        </div>
      </div>
    )
  }
})

export default SimpleForm
