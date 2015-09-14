
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
      config_options: []
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
        var file_header = response.objects[0].file_header
        self.setState({
          config_options: file_header.replace('"','').split(','),
        });
      })
    }

    reader.readAsDataURL(file);
  },

  _setDocConfig : function (config_val) {
    console.log(config_val)
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
      this._setDocConfig);

      if (headerList.length > 0) {
        var fileConfig = <div>
          <TitleMenu text="Unique ID Col">
            {headerList}
          </TitleMenu>
          <TitleMenu text="Region Column">
            {headerList}
          </TitleMenu>
          <TitleMenu text="Campaign Column">
            {headerList}
          </TitleMenu>
      </div>
      }
      else {
        var fileConfig = ''
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
        <input type="text" label="file name:" />
      </form>

      {fileConfig}

    </div>);
  },
});


module.exports = DocForm;
