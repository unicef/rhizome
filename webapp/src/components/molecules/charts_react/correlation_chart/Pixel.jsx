import React, { Component, PropTypes } from 'react'
import Layer from 'react-layer'
import d3 from 'd3'
import Tooltip from 'components/molecules/Tooltip'

class Pixel extends Component {

  color = d3.scale.linear()
    .domain([-1,0,1])
    .range(['blue','white','red'])

  handleMouseOver = (event) => {
  		//.html(d.i + ": " + label_row[d.i] + "<br>" + d.j + ": " + label_col[d.j] + "<br>" + "Value: " + (d.val > 0 ? "+" : "&nbsp") + d.val.toFixed(3))
    let tooltip = () => {
      return (
        <Tooltip left={event.pageX} top={event.pageY}>
          <div>{this.props.datum.val ? 'Missing value' : this.props.datum.val}</div>
        </Tooltip>
      )
    }

    if (!this.tip) {
      this.tip = new Layer(document.body, tooltip)
    }
    this.tip.render()
  }

  handleMouseOut = () => {
    if (this.tip) {
      this.tip.destroy()
      this.tip = null
    }
  }

  render () {
	  return (
	    <rect
	    	className={'pixel'}
	    	width={this.props.scale(0.9)}
	    	height={this.props.scale(0.9)}
	    	fill={this.color(this.props.datum.val)}
	    	onMouseOver={this.handleMouseOver}
	    	onMouseOut={this.handleMouseOut}
        x={this.props.x}
        y={this.props.y}
	    />
	  )
  }
}

Pixel.propTypes = {
  scale: PropTypes.func.isRequired,
  datum: PropTypes.shape({
    i: PropTypes.number,
    j: PropTypes.number,
    val: PropTypes.number
  }),
  labelSpace: PropTypes.number,
  x: PropTypes.number,
  y: PropTypes.number
}

Pixel.defaultProps = {
  scale: null,
  datum: null,
  labelSpace: 225,
  x: 300,
  y: 300
}

export default Pixel

// ORIGINAL
//---------------------------------------------------------------------------
// const pixel = matrix.selectAll('rect.pixel').data(corr_data)

// as of now, data not changable, only sortable
// pixel.enter()
// 	.append('rect')
// 	.attr('class', 'pixel')
// 	.attr('width', scale(0.9))
// 	.attr('height', scale(0.9))
// 	.style('fill',function(d){ return color(d.val)})
// 	.on('mouseover', function(d){pixel_mouseover(d)})
// 	.on('mouseout', function(d){mouseout(d)})
