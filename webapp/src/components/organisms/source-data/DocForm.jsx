import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import ExpandableMenuItem from 'components/atoms/dropdown/ExpandableMenuItem'
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

  onDrop: function (files) {
    if (files[0].name.endsWith('.csv') || files[0].name.endsWith('.xlsx') || files[0].name.endsWith('.xls')) {
      this.handleFile(files[0])
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
  handleFile: function (file) {
    var reader = new window.FileReader()

    reader.onload = function (upload) {
      DocFormActions.getData(file, upload)
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

  buildHeaderList: function (configType) {
    var stateHeader = this.state.config_options

    return ExpandableMenuItem.fromArray(
      _.map(stateHeader, d => {
        return {
          title: d.replace('"', ''),
          value: d.replace('"', '')
        }
      }),
      this.setDocConfig.bind('config_type', configType))
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

    var divZoneStyle = {
      border: '3px solid #426281'
    }

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
      fontSize: '1rem'
    }

    let uploadStyle = {
      padding: '0 30px'
    }

    // let tableMarginStyle = {
    //   marginTop: '50px'
    // }

    let dropZone = (
      <div>
        <div style={uploadStyle}>
          <div style={divZoneStyle} className='medium-12 columns'>
            <Dropzone onDrop={this.onDrop} style={dropZoneStyle}>
              <div style={uploadButtonStyle}>Choose to upload</div>
            </Dropzone>
          </div>
        </div>
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
