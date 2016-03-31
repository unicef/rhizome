import React from 'react'

export default React.createClass({
  propTypes: {
    initialText: React.PropTypes.string,
    save: React.PropTypes.func,
    className: React.PropTypes.string
  },

  getInitialState: function () {
    return {
      text: this.props.initialText
    }
  },

  componentDidMount: function () {
    React.findDOMNode(this.refs.title_input).focus()
  },

  componentWillReceiveProps: function (nextProps) {
    this.setState({text: nextProps.initialText})
  },

  _updateText: function (e) {
    this.setState({text: e.currentTarget.value})
  },

  saveTitle: function (event) {
    if (event.type === 'blur' || event.keyCode === 13 ) { // Keycode for 'Enter' key
      this.props.save(this.state.text)
    } else if (event.keyCode === 27) {
      this.props.save(null)
    }
  },

  render: function () {
    return (
      <form onSubmit={event => event.preventDefault()} className='title-input'>
        <input type='text'
          ref='title_input'
          className={this.props.className}
          value={this.state.text}
          onChange={this._updateText}
          onBlur={this.saveTitle}
          onKeyUp={this.saveTitle}
          placeholder='Enter Title'/>
          <button type='reset' className='button icon-button' onClick={() => this.props.save(null)} >
            <i className='fa fa-times'/>
          </button>
          <button
            className='button icon-button'
            onClick={(e) => {
              e.preventDefault()
              this.props.save(this.state.text)
            }}>
            <i className='fa fa-check'/>
          </button>
      </form>
    )
  }
})
