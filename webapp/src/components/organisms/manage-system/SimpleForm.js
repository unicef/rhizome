import api from 'data/api'
import React from 'react'
import page from 'page'
import Reflux from 'reflux'
import ReactJson from 'react-json'
import _ from 'lodash'

import SimpleFormStore from 'stores/SimpleFormStore'
import SimpleFormActions from 'actions/SimpleFormActions'
import SimpleFormComponent from './SimpleFormComponent'
import DropdownMenu from 'components/molecules/menus/DropdownMenu.jsx'

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
      tagTree: [],
      errorMessage: {},
      formData: {}
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

  findCurrentIndicatorId: function () {
    var mainID = this.props.params.id
    var data = this.refs.form_data.getValue()
    if (_.isEmpty(mainID)) {
      var dataObject = this.state.store.dataObject
      this.setState({
        formData: data,
        store: {
          dataObject: dataObject,
          loading: false,
          displayMsg: true,
          saveSuccess: false,
          message: 'Please save the indicator first before adding tags or calculations!'
        }
      })
    }
    return (!_.isEmpty(mainID))
  },

  addTagToIndicator: function (tag_id) {
    if (this.findCurrentIndicatorId()) {
      SimpleFormActions.addTagToIndicator(this.props.params.id, tag_id)
    }
  },

  addCalculationToIndicator: function (typeInfo, indicator_id) {
    if (this.findCurrentIndicatorId()) {
      SimpleFormActions.addCalculationToIndicator(this.props.params.id, indicator_id, typeInfo)
    }
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
  validateData: function (data) {
    var indicators = this.state.store.indicators
    var errorMessage = {}
    var maxLength = 255
    for (var key in data) {
      if (!data[key] && data[key] !== 0) {
        errorMessage[key] = key.toUpperCase() + ' can not be blank.'
      }
      if (data[key].length > maxLength) {
        errorMessage[key] = key.toUpperCase() + ' is too long.'
      }
    }

    if (!errorMessage['name'] & !this.props.params.id) {
      var result = _.find(indicators, d => {
        return d === data.name
      })
      if (result) {
        errorMessage['name'] = 'The indicator of this NAME already exists.'
      }
    }

    return errorMessage
  },
  onSubmit: function (e) {
    e.preventDefault()
    var data = this.refs.form_data.getValue()

    // if there is any data in the react-json form add it here //
    for (var key in this.state.extraFormData) {
      data[key] = this.state.extraFormData[key]
    }

    let errorMessage = this.validateData(data)

    _.isEmpty(errorMessage)
      ? SimpleFormActions.baseFormSave(this.props.params.id, this.props.params.contentType, data)
      : this.setState({
        errorMessage: errorMessage,
        formData: data
      })
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
    var formData = _.isEmpty(this.state.formData) ? this.state.store.formData : this.state.formData

    let message = this.state.store.displayMsg
      ? (
      <div className={`message${this.state.store.saveSuccess ? ' success' : ' error'}`}>
        {this.state.store.message}
      </div>
      )
      : null

    if (objectId && !dataObject) {
      if (this.state.store.loading) {
        return <div>
                 Loading MetaData Manager
               </div>
      } else {
        page('/manage_system/' + contentType + '/')
        return (
        <div>
          Error. There is no data received.
        </div>
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
          <p>
            {`Parent Tag: ${selected}`}
          </p>
          <br />
          <DropdownMenu
            items={tagTree}
            sendValue={this.setParentTag}
            item_plural_name='Parent Tags'
            text='Parent tag'
            icon='fa-tag' />
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

    if (this.state.store.saveSuccess) {
      setTimeout(() => {
        var newId = this.state.store.objectId
        this.state.store.displayMsg = false
        this.state.store.saveSuccess = false
        if (this.props.params && this.props.params.id) {
          page('/manage_system/' + (contentType === 'indicator_tag' ? 'tags' : 'indicators'))
        } else {
          page('/manage_system/manage/' + contentType + '/' + newId)
        }

        SimpleFormActions.initialize(newId, contentType)
      }, 500)
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
    if (contentType === 'indicator_tag') {
      subFormList = (
        <div>
          <SimpleFormComponent
            objectId={objectId}
            contentType={'indicator'}
            componentTitle='Add Indicators to Tags'
            onClick={this.addIndicatoToTag}
            smallItemCouldClick
            onSmallItemClick={this.removeTagFromIndicator} />
          <br />
          </div>
      )
    }

    return (
    <div className='row'>
      <div className='small-8 columns'>
        <div>
          <h2>Manage Admin Page</h2>
          {idInfo}
          {message}
          <ReactJson
            value={formData}
            settings={formSettings}
            errorMessage={this.state.errorMessage}
            ref='form_data' />
          {additionalFormComponents}
          <br />
          <button className='tiny' onClick={this.onSubmit}>
            Save
          </button>
        </div>
      </div>
      <div className='small-4 columns'>
        {subFormList}
      </div>
    </div>
    )
  }
})

export default SimpleForm
