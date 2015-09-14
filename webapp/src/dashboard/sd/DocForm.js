
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
      api.uploadPost({docfile:upload.target.result})
    }

    reader.readAsDataURL(file);
  },

  _setDocConfig : function (config_val) {
    console.log('-----====------')
    console.log(config_val)
    console.log('-----====------')
  	},


  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {

    var defaultHeader = 'test'
    var headerList = MenuItem.fromArray(
      _.map(['test','this','component'], d => {
        return {
          title : d,
          value : d
        };
      }),
      this._setDocConfig);

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
      <TitleMenu text={defaultHeader}>
        {headerList}
      </TitleMenu>

    </div>);
  },
});


module.exports = DocForm;
