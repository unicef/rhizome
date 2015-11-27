import _ from 'lodash'
import React from 'react'
import Reflux from 'reflux'
import moment from 'moment'

import ButtonMenu from 'component/ButtonMenu.jsx'

import MenuItem from 'component/MenuItem.jsx'
import Dropzone from 'react-dropzone'

import DocFormActions from 'actions/DocFormActions'
import DocFormStore from 'stores/DocFormStore'

var DocForm = React.createClass({
  // see here: https:// fitacular.com/blog/react/2014/06/23/react-file-upload-base64/

  mixins: [
    Reflux.connect(DocFormStore)
  ],

  propTypes: {
    location: React.PropTypes.object.isRequired,
    campaign: React.PropTypes.object,
    reviewTable: React.PropTypes.element,
    doc_title: React.PropTypes.string
  },

  // since we are starting off without any data, there is no initial value
  getInitialState: function () {
    return {
      data_uri: null,
      config_options: [],
      uq_id_column: null,
      location_column: null,
      campaign_column: null,
      created_doc_id: null,
      doc_detail_meta: null,
      doc_is_refreshed: false,
      new_doc_title: null
    }
  },

  onDrop: function (files) {
    this.handleFile(files[0])
  },

  // prevent form from submitting; we are going to capture the file contents
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

  setDocConfig: function (config_type, config_val) {
    var self = this

    var doc_detail_meta = self.state.doc_detail_meta
    var doc_detail_type = doc_detail_meta[config_type]
    var doc_detail_type_id = doc_detail_type['id']

    DocFormActions.setDocConfig({
      document_id: self.state.created_doc_id,
      doc_detail_type_id: doc_detail_type_id,
      doc_detail_value: config_val
    }, config_type)
  },

  syncDocData: function (config_val) {
    var self = this
    DocFormActions.transformUpload({document_id: self.state.created_doc_id})
  },

  buildHeaderList: function (config_type) {
    var state_header = this.state.config_options

    return MenuItem.fromArray(
      _.map(state_header, d => {
        return {
          title: d.replace('"', ''),
          value: d.replace('"', '')
        }
      }),
      this.setDocConfig.bind('config_type', config_type))
  },

  // return the structure to display and bind the onChange, onSubmit handlers
  render: function () {
    var uqHeaderList = this.buildHeaderList('uq_id_column')
    var rgHeaderList = this.buildHeaderList('location_column')
    var cpHeaderList = this.buildHeaderList('campaign_column')
    var location = _.get(this.props.location, 'location', this.props.location.name)
    var campaign = _.get(this.props.campaign, 'campaign', moment(this.props.campaign.start_date, 'YYYY-MM-DD').format('YYYY/MM'))

    var fileConfigForm = ''
    var uploadButton = ''
    if (this.state.created_doc_id) {
      fileConfigForm = (
        <ul>
          <li>
            <div className='large-8 medium-8 small-12 columns csv-upload__file--message'>Unique ID: (To be
              selected) {this.state.uq_id_column}</div>
            <ButtonMenu text={this.state.uq_id_column}
                        style='large-4 medium-4 small-12 columns csv-upload__button-style'>
              {uqHeaderList}
            </ButtonMenu>
          </li>
          <li>
            <div className='large-8 medium-8 small-12 columns csv-upload__file--message'>location: (To be
              selected) {this.state.location_column}</div>
            <ButtonMenu text={this.state.location_column}
                        style='large-4 medium-4 small-12 columns csv-upload__button-style'>
              {rgHeaderList}
            </ButtonMenu>
          </li>
          <li>
            <div className='large-8 medium-8 small-12 columns csv-upload__file--message'>Campaign: (To be
              selected) {this.state.campaign_column}</div>
            <ButtonMenu text={this.state.campaign_column}
                        style='large-4 medium-4 small-12 columns csv-upload__button-style'>
              {cpHeaderList}
            </ButtonMenu>
          </li>
        </ul>
      )

      if (this.state.uq_id_column && this.state.location_column && this.state.campaign_column) {
        let next_link = '/datapoints/source-data/' + [location, campaign].join('/') + '/viewraw/' + this.state.created_doc_id
        let [doc_name, doc_revision] = this.props.doc_title.split('-')


        uploadButton = this.state.doc_is_refreshed
          ? <a href={next_link} className='cd-button refresh__button--margin'> Review Upload</a>
          : <span className='cd-button refresh__button--margin' onClick={this.syncDocData}>Sync Data</span>

        fileConfigForm = this.state.doc_is_refreshed
          ? (<div>
          <div className='csv-upload__tags'>
            <span>File Name: </span>{doc_name}
          </div>
          <div className='csv-upload__tags'>
            <span>Revision: </span>{doc_revision}
          </div >

        </div>)
          : fileConfigForm
      }
    }


    //var reviewBtn = ''
    //if (this.state.uq_id_column && this.state.location_column && this.state.campaign_column && this.state.doc_is_refreshed) {
    //  var next_link = '/datapoints/source-data/' + [location, campaign].join('/') + '/viewraw/' + this.state.created_doc_id
    //  reviewBtn = <a href={next_link} className='cd-button refresh__button--margin'> Review Upload</a>
    //}

    var stepMessage = this.state.created_doc_id
      ? (<div>
      <span>STEP 2 </span>Please choose which columns in your uploaded data are ID, Location and Campaign.
    </div>)
      : (<div>
      <span>STEP 1 </span>Click the button upload a CSV file, or please drag and drop the file into the box.
    </div>)

    var divZoneStyle = {
      padding: '10px',
      border: '2px solid #426281'
    }

    var dropZoneStyle = {
      padding: '4rem 15rem'
    }

    var uploadButtonStyle = {
      backgroundColor: '#344B61',
      color: '#FEFEFE',
      textTransform: 'uppercase',
      textAlign: 'center',
      margin: '0 38%',
      padding: '15px',
      cursor: 'pointer',
      width: 200
    }

    let uploadStyle = {
      padding: '0 30px'
    }

    let tableMarginStyle = {
      marginTop: '50px'
    }

    let dropZone = (
      <div>
        <div style={uploadStyle}>
          <div style={divZoneStyle} className='medium-12 columns'>
            <Dropzone onDrop={this.onDrop} style={dropZoneStyle}>
              <div style={uploadButtonStyle}>Choose to upload</div>
            </Dropzone>
          </div>
        </div>
        <div className='medium-12 columns' style={tableMarginStyle}>
          {this.props.reviewTable}
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

    let uploadFile = this.state.created_doc_id ? fileChoose : dropZone

    // since JSX is case sensitive, be sure to use 'encType'
    return (
      <div>
        <div className='medium-12 columns upload__csv--step'>
          {stepMessage}
        </div>
        {uploadFile}
      </div>
    )
  }
})

export default DocForm
