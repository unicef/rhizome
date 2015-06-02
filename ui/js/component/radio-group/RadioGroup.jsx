var React  = require('react');

module.exports = React.createClass({
  propTypes: {
  	values: React.PropTypes.array.isRequired,
  	value: React.PropTypes.string.isRequired,
  	name: React.PropTypes.string.isRequired,
  	onChange: React.PropTypes.func.isRequired,
  	horizontal: React.PropTypes.bool
  },
  getDefaultProps: function() {
      return {
        horizontal: false
      };
    },
  _handleChange: function(event){
    this.props.onChange(event.target.value);
  },
  render: function(){
      var self = this;
      var radios = this.props.values.map(function(radio){
      	return <div key={radio.value} className={self.props.horizontal?"horizontal":null}><input type="radio" name={self.props.name} value={radio.value} 
      						checked={self.props.value == radio.value ? "checked" : false} 
      						onChange={self._handleChange}/> {radio.title}</div>
      });
      return (<div className="radioGroupContainer">{radios}</div>);
  }
});