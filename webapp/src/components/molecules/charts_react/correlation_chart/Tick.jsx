import React, { Component, PropTypes } from 'react'
import d3 from 'd3'

class Tick extends Component {
  handleClick = (event) => {
    this.props.handleClick(this.props.index)
  }

  render = () => {
    const textTransformString = 'rotate(270 ' + this.props.position + ',0)'
    const styles = {
      textAnchor: this.props.textAnchor,
      fontSize: this.props.fontSize
    }
    return (
      <text
        className='tick'
        style={styles}
        onMouseOver={this.props.handleMouseOver}
        onMouseOut={this.props.handleMouseOut}
        onClick={this.handleClick}
        x={this.props.x}
        y={this.props.y}>
        {this.props.text}
      </text>
    )
  }
}

Tick.propTypes = {
  text: PropTypes.string,
  textAnchor: PropTypes.string,
  index: PropTypes.number,
  fontSize: PropTypes.number,
  handleMouseOver: PropTypes.func,
  handleMouseOut: PropTypes.func,
  handleClick: PropTypes.func,
  position: PropTypes.number,
  x: PropTypes.number,
  y: PropTypes.number
}

Tick.getDefaultProps = {
  text: 'N/A',
  textAnchor: 'start',
  index: 0,
  fontSize: 12,
  position: 0,
  handleMouseOver: null,
  handleMouseOut: null,
  handleClick: null,
  x: null,
  y: null
}

export default Tick

// ORIGINAL
//---------------------------------------------------------------------------
// tick_col.enter()
//   .append('text')
//   .attr('class','tick')
//   .style('text-anchor', 'start')
//   .attr('transform', function(d, i){return 'rotate(270 ' + labelCol(order_col[i] + 0.7) + ',0)'})
//   .attr('font-size', scale(0.8))
//   .text(function(d){ return d })
//   .on('mouseover', function(d, i){tick_mouseover(d, i, col[i], label_row)})
//   .on('mouseout', function(d){mouseout(d)})
//   .on('click', function(d, i){reorder_matrix(i, 'col')})
