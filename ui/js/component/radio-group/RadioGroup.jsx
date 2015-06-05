var React  = require('react');

module.exports = React.createClass({
  propTypes: {
  	values: React.PropTypes.array.isRequired,
  	value: React.PropTypes.number.isRequired,
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
      var radios = this.props.values.map(function(radio,index){
      	return <div key={radio.value} className={self.props.horizontal?"horizontal":null}><input type="radio" name={self.props.name} value={radio.value} 
      						checked={self.props.value == index ? "checked" : false} 
      						onChange={self.props.onChange.bind(null,index)}/> {radio.title}</div>
      });
      return (<div className="radioGroupContainer">{radios}</div>);
  }
});