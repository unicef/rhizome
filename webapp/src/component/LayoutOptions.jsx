var React = require('react');

module.exports = React.createClass({
  propTypes: {
    values: React.PropTypes.array.isRequired,
    value: React.PropTypes.number.isRequired,
    onChange: React.PropTypes.func.isRequired
  },
  _handleChange: function (event) {
    this.props.onChange(event.target.value);
  },
  render: function () {
    var self = this;
    var radios = this.props.values.map(function (radio) {
      var radioID = "layoutOption-" + radio.value;
      return <div key={radio.value}
                  className={self.props.value == radio.value ? 'active' : 'inactive'}>
        <input type="radio"
               name={radio.name}
               value={radio.value}
               checked={self.props.value == radio.value ? "checked" : false}
               onChange={self._handleChange.bind(radio)}
               id = {radioID}
          />

        <label htmlFor={radioID}>
          <h3>{radio.name}</h3>
          <img src={radio.src} alt=""/>
        </label>
      </div>


    });
    return (<div className="LayoutOptionsContainer">{radios}</div>);
  }
});