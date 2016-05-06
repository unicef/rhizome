import React from 'react'

const ColorSwatch = React.createClass({
  render () {
  	const item = this.props.item
	  const colorList = item.colors.map(color => {
	    const style = {backgroundColor: color}
	    return (
	      <span key={item.value + color} className='palette-picker__color' style={style}>&nbsp;</span>
	    )
	  })
		return (
			<span className='color-swatch'>
				{ colorList }
			</span>
		)
  }
})

export default ColorSwatch
