
var React		= require('react');
var DocForm = React.createClass({

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

    var x = 'test'

    reader.onload = function(upload) {
      self.setState({
        data_uri: upload.target.result,
      });
    }

    reader.readAsDataURL(file);
  },

  // return the structure to display and bind the onChange, onSubmit handlers
  render: function() {

    // since JSX is case sensitive, be sure to use 'encType'
    return (
      <form onSubmit={this.handleSubmit} encType="multipart/form-data">
        <input type="file" onChange={this.handleFile} />
      </form>
    );
  },
});


module.exports = DocForm;
