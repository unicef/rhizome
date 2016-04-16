import React from 'react'
import _ from 'lodash'

import palettes from 'utilities/palettes'

class PaletteSelector extends React.Component {
  constructor (props) {
    super(props)
  }

  static defaultProps = {
    value: 0,
    onChange: () => {}
  }

  static propTypes = {
    value: React.PropTypes.oneOfType([
      React.PropTypes.string,
      React.PropTypes.number
    ]),
    onChange: React.PropTypes.func
  }

  render () {
    let paletteList = _.map(palettes, (value, key) => {
      let colorList = value.slice(0, 8).map(color => {
        let style = {
          backgroundColor: color
        }
        return (
          <span key={value + key + color} className='palette-picker__color' style={style}>&nbsp;</span>
        )
      })
      return (
        <div key={value + key} className={`palette-picker__palette-group${this.props.value === key ? ' active' : ''}`}>
          <input type='radio' name='palette' id={key}
            value={key}
            checked={this.props.value === key ? 'checked' : false}
            onChange={this.props.onChange.bind(null, key)}/>
          <label className='palette-picker__palette' htmlFor={key}>
            {colorList}
          </label>
        </div>
      )
    })
    return (
      <div className='palette-picker'>
        {paletteList}
      </div>
    )
  }
}

export default PaletteSelector
