import React, { Component, PropTypes } from 'react'
import Tick from 'components/molecules/dimacharts/Tick'
import d3 from 'd3'

class TickRow extends Component {

  handleMouseOver = (event) => {
    // console.log('tick moused over')
	  // .on('mouseover', function(d, i){tick_mouseover(d, i, row[i], label_col)})
  }

  handleMouseOut = () => {
    // console.log('tick moused out')
	  // .on('mouseout', function(d){mouseout(d)})
  }

  handleClick = (tickPosition) => {
    this.props.handleClick(tickPosition, 'row')
  }

  render = () => {
   const props = this.props
   const newLabelSpace = props.labelSpace + 10
   const transformString = `translate(${props.labelSpace}, ${newLabelSpace})`
   const ticks = props.rowLabels.map((rowLabel, index) => {
      const position = props.scale(props.rowOrder[index] + 0.7)
      return (
        <Tick
          text={rowLabel}
          fontSize={props.scale(0.8)}
          textAnchor='start'
          index={index}
          position={position}
          handleMouseOver={this.handleMouseOver}
          handleMouseOut={this.handleMouseOut}
          handleClick={this.handleClick}
          x={position}
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

TickRow.propTypes = {
  rowLabels: PropTypes.array,
  scale: PropTypes.func,
  handleClick: PropTypes.func,
  rowOrder: PropTypes.array
}

TickRow.getDefaultProps = {
  rowLabels: [],
  handleClick: null,
  scale: null,
  rowOrder: []
}

export default TickRow

// ORIGINAL
//---------------------------------------------------------------------------
// tick_row = svg.append('g')
//   .attr('class','ticks')
//   .attr('transform', 'translate(' + (label_space) + ',' + (label_space + 10) + ')')
//   .selectAll('text.tick')
//   .data(label_row)

// tick_row.enter()
//   .append('text')
//   .attr('class','tick')
//   .style('text-anchor', 'end')
//   .attr('font-size', scale(0.8))
//   .text(function(d){ return d })
//   .on('mouseover', function(d, i){tick_mouseover(d, i, row[i], label_col)})
//   .on('mouseout', function(d){mouseout(d)})
//   .on('click', function(d, i){reorder_matrix(i, 'row')})

