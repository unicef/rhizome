import d3 from 'd3'
import React, { Component, PropTypes } from 'react'
import D3Chart from '02-molecules/dimacharts/D3Chart'
import Matrix from '02-molecules/dimacharts/Matrix'
import TickCol from '02-molecules/dimacharts/TickCol'
import TickRow from '02-molecules/dimacharts/TickRow'

class CorrelationChart extends Component {

  constructor(props) {
    super(props)
    this.state = {
      colOrder: d3.range(props.colLabels.length + 1),
      rowOrder: d3.range(props.rowLabels.length + 1)
    }
  }

  getScale = (value) => {
    const scale = d3.scale.linear()
      .domain([0, d3.min([50, d3.max([this.props.colLabels.length, this.props.rowLabels.length, 4])])])
      .range([0, this.props.zoomValue * 600])
    return scale(value)
  }

  indexify = (mat) => {
    let res = []
    for(let i = 0; i < mat.length; i++){
      for(let j = 0; j < mat[0].length; j++){
        res.push({i:i, j:j, val:mat[i][j]})
      }
    }
    return res
  }

  // const last_k = 0
  // const last_what = 'col'
  reorderMatrix = (k, what, rowOrder, colOrder) => {
    const row = this.props.corrData
    const col = d3.transpose(this.props.corrData)
    let last_k = k
    let last_what = what
    let order = []
    let vec = []
    let labels = []
    let vecs = []
    if (what === 'row') {  //yes, we are sorting counterpart
      vec = row[k]
      vecs = row
      labels = this.props.colLabels  //test is if it ok
    } else if ( what === 'col' ) {
      vec = col[k]
      vecs = col
      labels = this.props.rowLabels
    }
    let indices = d3.range(vec.length)
    const sort_process = 'value' // create a dropdwon to choose
    switch (sort_process) {
      case "value":
      indices = indices.sort((a,b) => { return vec[b] - vec[a]})
      break
      case "abs_value":
      indices = indices.sort((a,b) => { return Math.abs(vec[b]) - Math.abs(vec[a])})
      break
      case "original":
      break
      case "alphabetic":
      indices = indices.sort((a,b) => { return Number(labels[a] > labels[b]) - 0.5})
      break
      case "similarity":
      // Ugly, but sometimes we want to sort the coordinate we have clicked
      // Also, as of now with no normalization etc
      indices = d3.range(vecs.length)
      indices = indices.sort((a,b) => {
        let s = 0
        for (let i = 0; i < vec.length; i++) {
          s += (vecs[b][i] - vecs[a][i]) * vec[i]
        }
        return s
      })
      const keep_symmetry = false // Hard coded for now. should be checkbox
      if (what === 'col' || keep_symmetry) {
        colOrder = this.reversePermutation(indices)
        console.log('1colOrder', colOrder)
      } //not else if!
      if ( what === 'row' || keep_symmetry) {
        rowOrder = this.reversePermutation(indices)
        console.log('2rowOrder', rowOrder)
      }
      this.setState({rowOrder: rowOrder, colOrder: colOrder})
      return undefined
    }
    if (what === 'row' || keep_symmetry) {
      console.log('3colOrder', colOrder)
      colOrder = this.reversePermutation(indices)
     } //not else if!
    if ( what === 'col' || keep_symmetry) {
      console.log('4rowOrder', rowOrder)
      rowOrder = this.reversePermutation(indices)
    }
    this.setState({rowOrder: rowOrder, colOrder: colOrder})
  }

  reversePermutation = (vec) =>{
    let res = []
    for (let i = 0; i < vec.length; i++) {
      res[vec[i]] = i
    }
    return res
  }

  render = () => {
    const props = this.props
    const corrData = this.indexify(props.corrData)
    return (
      <D3Chart width={props.width} height={props.height}>
        <Matrix corrData={corrData} scale={this.getScale} labelSpace={props.labelSpace} colOrder={this.state.colOrder} rowOrder={this.state.rowOrder} />
        <TickCol
          colLabels={props.colLabels}
          scale={this.getScale}
          labelSpace={props.labelSpace}
          colOrder={this.state.colOrder}
          handleClick={colPosition => this.reorderMatrix(colPosition, 'col')}
        />
        <TickRow
          rowLabels={props.rowLabels}
          scale={this.getScale}
          labelSpace={props.labelSpace}
          rowOrder={this.state.rowOrder}
          handleClick={rowPosition => this.reorderMatrix(rowPosition, 'row')}
         />
      </D3Chart>
    )
  }
}

CorrelationChart.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
  zoomValue: PropTypes.number,
  corrData: PropTypes.array,
  colLabels: PropTypes.array,
  rowLabels: PropTypes.array,
  labelSpace: PropTypes.array
}

CorrelationChart.defaultProps = {
  width: 600,
  height: 600,
  colLabels: ['one', 'two', 'three'],
  rowLabels: ['apple', 'orange', 'banana'],
  corrData: [1, 2, 3, 4, 5, 6],
  zoomValue: .5,
  labelSpace: 255
  // zoomValue = parseFloat(d3.select('input#zoom')[0][0].value)   -- // Add later to control with field
}

export default CorrelationChart

// ORIGINAL
//---------------------------------------------------------------------------
// const scale = d3.scale.linear()
// .domain([0, d3.min([50, d3.max([label_col.length, label_row.length, 4])])])
// .range([0, parseFloat(d3.select("input#zoom")[0][0].value) * 600])
