import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import ExpandableMenuItem from 'components/dropdown/ExpandableMenuItem'
import Dropzone from 'react-dropzone'
import ReactJson from 'react-json'

import DocFormActions from 'actions/DocFormActions'
import DocFormStore from 'stores/DocFormStore'

var DocForm = React.createClass({
  mixins: [
    Reflux.connect(DocFormStore)
  ],

  propTypes: {},

  getInitialState: function () {
    return {
      data_uri: null,
      config_options: [],
      created_doc_id: null,
      doc_detail_meta: null,
      doc_is_refreshed: false,
      new_doc_title: null,
      is_odk_config_form: false,
      errorMessage: ''
      // uq_id_column: null,
      // location_column: null,
      // date_column: null,
    }
  },

  endsWith: function (str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1
  },

  onDropDateData: function (files){
      console.log('onDropMultiCampaign')
      this.setState({'file_type':'date_data'})
      this.onDrop(files[0], 'date')
  },

  onDropCampaign: function (files){
      console.log('onDropCampaign')
      this.setState({'file_type':'campaign'})
      this.onDrop(files[0], 'campaign')
  },

  onDrop: function (file, file_type) {
    if (file.name.endsWith('.csv') || file.name.endsWith('.xlsx') || file.name.endsWith('.xls')) {
      this.handleFile(file, file_type)
    } else {
      this.setState({
        errorMessage: 'Please upload a .csv, .xls or .xlsx file.'
      })
    }
  },

  handleSubmit: function (e) {
    e.preventDefault()
  },

  // when a file is passed to the input field, retrieve the contents as a
  // base64-encoded data URI and save it to the component's state
  handleFile: function (file, file_type) {
    var reader = new window.FileReader()

    reader.onload = function (upload) {
      DocFormActions.getData(file, upload, file_type)
    }
    reader.readAsDataURL(file)
  },

  setDocConfig: function (configType, configValue) {
    var docDetailMeta = this.state.doc_detail_meta
    var docDetailType = docDetailMeta[configType]
    var docDetailTypeId = docDetailType['id']

    DocFormActions.setDocConfig({
      document_id: this.state.created_doc_id,
      doc_detail_type_id: docDetailTypeId,
      doc_detail_value: configValue
    }, configType)
  },

  syncDocData: function () {
    DocFormActions.transformUpload({document_id: this.state.created_doc_id})
  },

  setOdkConfig: function () {
    this.setState({is_odk_config_form: true})
  },

  processOdkForm: function (e) {
    var data = this.refs.form_data.getValue()
    DocFormActions.setOdkFormName(data)
  },

  render: function () {
    var fileConfigForm = ''
    var syncUploadButton = <a disabled={this.state.isRefreshing} className='button button-refresh'
       onClick={this.syncDocData}> <i className='fa fa-refresh'></i>{ this.state.isRefreshing ? ' ' : 'Sync Data'}
    </a>

    let uploadButton = ''
    if (this.state.created_doc_id) {
      let nextLink = '/source-data/viewraw/' + this.state.created_doc_id
      uploadButton = this.state.doc_is_refreshed
          ? <a href={nextLink} className='cd-button refresh__button--margin'>Review</a>
          : syncUploadButton
    }
    var errorMessage = (
        <div className='error'>{this.state.errorMessage}</div>
      )

    var dropZoneStyle = {
      padding: '4rem 0',
      display: 'flex',
      justifyContent: 'center'
    }

    var uploadButtonStyle = {
      backgroundColor: '#344B61',
      color: '#FEFEFE',
      textTransform: 'uppercase',
      padding: '15px',
      cursor: 'pointer',
      minWidth: 200,
      fontFamily: 'adelle',
      fontSize: '1rem',
      textAlign: 'center'
    }

    var borderStyle = {border: '3px solid #426281'}

    let dropZoneDate = (
      <div>
          <div style={borderStyle} className='medium-12 columns'>
            <Dropzone onDrop={this.onDropDateData} style={dropZoneStyle}>
              <div style={uploadButtonStyle}>Date Data</div>
            </Dropzone>
          </div>
        </div>
    )

    let dropZoneCampaign = (
      <div>
          <div style={borderStyle} className='medium-12 columns'>
            <Dropzone onDrop={this.onDropCampaign} style={dropZoneStyle}>
              <div style={uploadButtonStyle}>Campaign Data</div>
            </Dropzone>
          </div>
        </div>
    )

    let dropZone = (
      <div className='row'>
        <div className='medium-6 columns'> {dropZoneDate} </div>
        <div className='medium-6 columns'> {dropZoneCampaign} </div>
      </div>
    )

    let fileChoose = (
      <div className='large-6 medium-8 small-12 columns upload__csv--file-choose'>
        {fileConfigForm}
        <div className='large-12 medium-12 small-12 columns refresh__button'>
          {uploadButton}
        </div>
      </div>
    )

    let odkForm = (
        <div className='row'>
          <ReactJson value={{'odk_form_id': ''}} settings={{'form': true, fields: {'odk_form_id': {type: 'string'}}}} ref='form_data'/>
          <br/>
          <button className='tiny' style={{ textAlign: 'right' }} onClick={ this.processOdkForm}>Process ODK Form</button>
        </div>
    )

    // if this is an odk_config form, render ODK form, else, render dropZone
    let baseFileForm = this.state.is_odk_config_form ? odkForm : dropZone
    let formComponent = this.state.created_doc_id ? fileChoose : baseFileForm

    return (
      <div>
        <div className='medium-12 columns upload__csv--step'>
          {errorMessage}
        </div>
        {formComponent}
      </div>
    )
  }
})

export default DocForm
