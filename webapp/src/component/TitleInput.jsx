var React = require('react')

module.exports = React.createClass({
  propTypes: {
    initialText: React.PropTypes.string,
    class: React.PropTypes.string,
    save: React.PropTypes.function,
  },

  getInitialState: function (){
    return {
      text: this.props.initialText
    }
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({text: nextProps.initialText})
  },

  _updateText: function (e){
    this.props.save(e.currentTarget.value)
    this.setState({text: e.currentTarget.value})
  },
  render: function (){
    return (<input type='text' className={this.props.class} value={this.state.text} onChange={this._updateText}/>)
  }
})
