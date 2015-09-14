
var _     	= require('lodash');
var React		= require('react');
var api 		= require('data/api.js')
var TitleMenu  	= require('component/TitleMenu.jsx');
var MenuItem    = require('component/MenuItem.jsx');


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
      created_doc_id: null
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
    }

    reader.readAsDataURL(file);
  },

  setDocConfig : function (config_val) {
    var self = this;
    var doc_id = this.state.doc_id;

    api.docDetailPost({
        document_id: this.state.created_doc_id,
        doc_detail_type_id:6,
        doc_detail_value: config_val
    }).then(function (response) {
      self.setState({
        uq_id_column: response.objects[0].doc_detail_value,
      });
    })
    console.log('=====')
    console.log(this.state.uq_id_column)
  	},

  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {

    var state_header = this.state.config_options

    var headerList = MenuItem.fromArray(
      _.map(state_header, d => {
        return {
          title : d,
          value : d
        };
      }),
      this.setDocConfig);

      if (headerList.length > 0) {
        var uq_col = "Unique ID Col" || this.state.uq_id_column
        var rg_col = "Region Col"
        var cp_col = "Campaign Col"

        var fileConfigForm = <form action={this.handleSubmit}>

        <TitleMenu text={uq_col}>
          {headerList}
        </TitleMenu>

        <TitleMenu text= {rg_col}>
          {headerList}
        </TitleMenu>

        <TitleMenu text= {cp_col}>
          {headerList}
        </TitleMenu>
      </form>
      }
      else {
        var fileConfigForm = ''
      }

    // since JSX is case sensitive, be sure to use 'encType'
    return (<div>
      <h6>Upload New File</h6>
      <form
        onSubmit={this.handleSubmit}
        encType="multipart/form-data"
        className="form"
        method="post"
        style={{ textAlign: 'right' }}
      >
        <input type="file" onChange={this.handleFile} className="upload" />
      </form>

      {fileConfigForm}

    </div>);
  },
});


module.exports = DocForm;
