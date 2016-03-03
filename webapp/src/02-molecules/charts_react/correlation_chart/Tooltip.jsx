import React, { Component } from 'react'

class Tooltip extends Component {

  render () {
  	const = styles {
  		opacity: '0.8',
  		left: this.props.xPos + 'px',
  		right: this.props.yPos + 'px'
  	}
    return (
    	<div style={styles}>
    		{this.props.children}
    	</div>
    )
  }
}

Pixel.propTypes = {
  xPos: PropTypes.number,
  yPos: PropTypes.number
}

Pixel.defaultProps = {
  xPos: 400,
  yPos: 400
}

export default Tooltip
