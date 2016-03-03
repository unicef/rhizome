import React, { Component, PropTypes } from 'react'
import Pixel from '02-molecules/dimacharts/Pixel'

class Matrix extends Component {

  render () {
    const props = this.props
    const newLabelSpace = props.labelSpace + 10
    const transform_string = `translate(${newLabelSpace}, ${newLabelSpace})`
    const pixels = props.corrData.map(dataValue => {
      const x = props.scale(props.colOrder[dataValue.j])
      const y = props.scale(props.rowOrder[dataValue.i])
      return (
        <Pixel
          datum={dataValue}
          scale={props.scale}
          x={x}
          y={y}
        />
      )
   })
   return (
      <g className={'matrix'} scale={this.props.scale} transform={transform_string}>
        { pixels }
      </g>
    )
  }
}

Matrix.propTypes = {
  scale: PropTypes.func.isRequired,
  labelSpace: PropTypes.number,
  corrData: PropTypes.array,
  colOrder: PropTypes.array,
  rowOrder: PropTypes.array
}

Matrix.getDefaultProps = {
  scale: null,
  labelSpace: 225,
  corrData: [],
  colOrder: [],
  rowOrder: []
}

export default Matrix

// ORIGINAL
//---------------------------------------------------------------------------
// const matrix = svg.append('g')
// .attr('class','matrix')
// .attr('transform', 'translate(' + (label_space + 10) + ',' + (label_space + 10) + ')')