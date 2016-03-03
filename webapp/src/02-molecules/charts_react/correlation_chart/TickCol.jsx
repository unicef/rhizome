import React, { Component, PropTypes } from 'react'
import Tick from '02-molecules/dimacharts/Tick'
import d3 from 'd3'

class TickCol extends Component {

  handleMouseOver = (event) => {
    // console.log('tick moused over')
    // .on('mouseover', function(d, i){tick_mouseover(d, i, row[i], label_col)})
  }

  handleMouseOut = () => {
    // console.log('tick moused out')
    // .on('mouseout', function(d){mouseout(d)})
  }

  handleClick = (tickPosition) => {
    console.log(tickPosition)
    this.props.handleClick(tickPosition, 'row')
  }

  render = () => {
    const props = this.props
    const newLabelSpace = props.labelSpace + 10
    const transformString = `translate(${newLabelSpace}, ${props.labelSpace})`
    const ticks = props.colLabels.map((columnLabel, index) => {
      const position = props.scale(props.colOrder[index] + 0.7)
      return (
        <Tick
          text={columnLabel}
          fontSize={props.scale(0.8)}
          textAnchor='end'
          index={index}
          position={position}
          handleMouseOver={this.handleMouseOver}
          handleMouseOut={this.handleMouseOut}
          handleClick={this.handleClick}
          y={position}
        />
      )
   })
   return (
      <g className={'ticks'} transform={transformString}>
      { ticks }
      </g>
    )
  }
}

TickCol.propTypes = {
  colLabels: PropTypes.array,
  scale: PropTypes.func,
  handleClick: PropTypes.func,
  colOrder: PropTypes.array
}

TickCol.getDefaultProps = {
  colLabels: [],
  scale: null,
  handleClick: null,
  colOrder: []
}

export default TickCol

// ORIGINAL
//---------------------------------------------------------------------------
// tick_col = svg.append('g')
//   .attr('class','ticks')
//   .attr('transform', 'translate(' + (label_space + 10) + ',' + (label_space) + ')')
//   .selectAll('text.tick')
//   .data(label_col)

// tick_col.enter()
//   .append('text')
//   .attr('class','tick')
//   .style('text-anchor', 'start')
//   .attr('transform', function(d, i){return 'rotate(270 ' + colLabels(order_col[i] + 0.7) + ',0)'})
//   .attr('font-size', scale(0.8))
//   .text(function(d){ return d })
//   .on('mouseover', function(d, i){tick_mouseover(d, i, col[i], label_row)})
//   .on('mouseout', function(d){mouseout(d)})
//   .on('click', function(d, i){reorder_matrix(i, 'col')})
