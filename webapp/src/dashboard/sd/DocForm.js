
var _     	= require('lodash');
var React		= require('react');
var api 		= require('data/api.js')
var TitleMenu  	= require('component/TitleMenu.jsx');
var MenuItem    = require('component/MenuItem.jsx');
var FileInput = require('react-file-input');
var Dropzone = require("dropzone");


var DocForm = React.createClass({
// see here: https://fitacular.com/blog/react/2014/06/23/react-file-upload-base64/

  // since we are starting off without any data, there is no initial value
  getInitialState: function() {
    return {
      data_uri: null,
      config_options: [],
      uq_id_column: null,
      region_column: null,
      campaign_column: null,
      created_doc_id: null,
      doc_detail_meta: null,
      doc_is_refreshed: false,
    };
  },

  // prevent form from submitting; we are going to capture the file contents
  handleSubmit: function(e) {
    e.preventDefault();
  },

  // when a file is passed to the input field, retrieve the contents as a
  // base64-encoded data URI and save it to the component's state
  handleFile: function(e) {
    var self = this;
    var reader = new FileReader();
    var file = e.target.files[0];

    reader.onload = function(upload) {
      self.setState({
        data_uri: upload.target.result,
      });

      api.uploadPost({docfile:upload.target.result}).then(function (response) {
        var response = response.objects[0]
        self.setState({
          config_options: response.file_header.replace('"','').split(','),
          created_doc_id: response.id
        });
      })

      api.docDetailType().then(function (response) {
        var doc_detail_types = response.objects
        self.setState({doc_detail_meta:doc_detail_types})
      })
    }
    reader.readAsDataURL(file);
  },

  setCpConfig :function (config_val) {
    var self = this;

    api.docDetailPost({
          document_id: this.state.created_doc_id,
          doc_detail_type_id: 4, // FIXME!!!!!! cp_doc_detail_type_id,
          doc_detail_value: config_val
    }).then(function (response) {
        var selected_cp_id = response.objects[0].doc_detail_value
        self.setState({campaign_column:selected_cp_id})
      });
  },

  setRgConfig :function (config_val) {
    var self = this;

    api.docDetailPost({
          document_id: this.state.created_doc_id,
          doc_detail_type_id: 3, // FIXME!!!!!! rg_doc_detail_type_id,
          doc_detail_value: config_val
    }).then(function (response) {
        var selected_rg_id = response.objects[0].doc_detail_value
        self.setState({region_column:selected_rg_id})
      });
  },

  setUqConfig : function (config_val) {
    var self = this;

    // FIXME uncaught TypeError: Cannot read property 'find' of undefined
    // var uq_doc_detail_type_id = self.state._.find(this.state.docDetailMeta, d => d.name === 'uq_id_column').id;

    api.docDetailPost({
          document_id: this.state.created_doc_id,
          doc_detail_type_id: 6, // FIXME!!!!!! uq_doc_detail_type_id,
          doc_detail_value: config_val
    }).then(function (response) {
        var selected_uq_id = response.objects[0].doc_detail_value
        self.setState({uq_id_column:selected_uq_id})
      });
  },

  syncDocData : function (config_val) {
      var self = this;

      api.transformUpload({document_id: this.state.created_doc_id})
      .then(function (response) {
          self.setState({doc_is_refreshed: true})
      });
  },

  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {


    var state_header = this.state.config_options

    var uqHeaderList = MenuItem.fromArray(
      _.map(state_header, d => {
        return {
          title : d,
          value : d
        };
      }),
      this.setUqConfig);

    var rgHeaderList = MenuItem.fromArray(
      _.map(state_header, d => {
        return {
          title : d,
          value : d
        };
      }),
      this.setRgConfig);

    var cpHeaderList = MenuItem.fromArray(
      _.map(state_header, d => {
        return {
          title : d,
          value : d
        };
      }),
      this.setCpConfig);

      if (this.state.created_doc_id) {
        var uq_col = this.state.uq_id_column
        var rg_col = this.state.region_column
        var cp_col = this.state.campaign_column

        var fileConfigForm = <div>
        <ul>
        <li>
          Unique ID Column:
          <TitleMenu text={uq_col}>
            {uqHeaderList}
          </TitleMenu>
        </li>
        <li>
          Region Code Column:
            <TitleMenu text={rg_col}>
              {rgHeaderList}
            </TitleMenu>
        </li>
        <li>
          Campaign Code Column:
            <TitleMenu text= {cp_col}>
              {cpHeaderList}
            </TitleMenu>
        </li>
      </ul>
    </div>
      }
      else {
        var fileConfigForm = ''
      }

      if (this.state.uq_id_column && this.state.region_column && this.state.campaign_column){
        var refreshBtn = <button onClick={this.syncDocData}> Sync Data</button>
      }
      else {
        var refreshBtn = ''
      }


    if (this.state.uq_id_column && this.state.region_column && this.state.campaign_column && this.state.doc_is_refreshed){
      var next_link = "viewraw/" + this.state.created_doc_id;
      var reviewBtn = <a href={next_link}  className="button"> Review Upload</a>
    }
    else {
      var reviewBtn = ''
    }


    // since JSX is case sensitive, be sure to use 'encType'
    return (<div>
      <form
        onSubmit={this.handleSubmit}
        encType="multipart/form-data"
        className="form"
      >
      <FileInput name="sourceUpload"
                 accept=".csv,.xls,.xlsx"
                 placeholder="Click here to Upload a New File"
                 className="inputClass"
                 onChange={this.handleFile} />
      </form>

      {fileConfigForm}
      {refreshBtn}
      {reviewBtn}

    </div>);
  },
});


module.exports = DocForm;
