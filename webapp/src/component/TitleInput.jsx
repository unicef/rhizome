import React from 'react'

export default React.createClass({
  propTypes: {
    initialText: React.PropTypes.string,
    save: React.PropTypes.func,
    class: React.PropTypes.string
  },

  getInitialState: function () {
    return {
      text: this.props.initialText
    }
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({text: nextProps.initialText})
  },

  _updateText: function (e) {
    this.props.save(e.currentTarget.value)
    this.setState({text: e.currentTarget.value})
  },
  render: function () {
    return (<input type='text' className={this.props.className} value={this.state.text} onChange={this._updateText}/>)
  }
})
