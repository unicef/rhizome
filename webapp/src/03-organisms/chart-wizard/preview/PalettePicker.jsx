import React from 'react'
import _ from 'lodash'

import palettes from '02-molecules/charts_d3/utils/palettes'

class PalettePicker extends React.Component {
  constructor (props) {
    super(props)
  }

  static defaultProps = {
    value: 0,
    onChange: () => {}
  }

  static propTypes = {
    value: React.PropTypes.number,
    onChange: React.PropTypes.func
  }

  render () {
    let paletteList = _.map(palettes, (value, key) => {
      let colourList = value.slice(0, 8).map(colour => {
        let style = {
          backgroundColor: colour
        }
        return (
          <span className='palette-picker__color' style={style}>&nbsp;</span>
        )
      })
      return (
        <div className={`palette-picker__palette-group${this.props.value === key ? ' active' : ''}`}>
          <input type='radio' name='palette' id={key}
            value={key}
            checked={this.props.value === key ? 'checked' : false}
            onChange={this.props.onChange.bind(null, key)}/>
          <label className='palette-picker__palette' htmlFor={key}>
            {colourList}
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

export default PalettePicker
