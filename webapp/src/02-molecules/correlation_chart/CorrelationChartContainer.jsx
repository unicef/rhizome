import React, { Component } from 'react'
import CorrelationChart from '02-molecules/dimacharts/CorrelationChart'

class CorrelationChartContainer extends Component {

  render () {
    const tempData = js_comparison_table()
    return (
      <div>
        <h4>Correlation Chart Container</h4>
        <CorrelationChart
          corrData={tempData.rows}
          colLabels={tempData.labels}
          rowLabels={tempData.labels}
        />
      </div>
    )
  }
}




const js_comparison_table = () => {
  const values = [true, false, 'true', 'false', 1, 0, -1, '1', '0', '-1', null, undefined, [], [[]], [0], [1], ['0'], ['1'], '', Infinity, -Infinity, NaN, {}]
  const values2 = [true, false, 'true', 'false', 1, 0, -1, '1', '0', '-1', null, undefined, [], [[]], [0], [1], ['0'], ['1'], '', Infinity, -Infinity, NaN, {}]
  // as for objects it makes difference if they are the same
  let rows = []
  let row = []
  let i
  let j
  let val1
  let val2

  row = values2.map(Boolean).map(x => {
    return x ? 1 : -0.5
  })
  rows.push([1].concat(row))
  for (i = 0; i < values.length; i++) {
    row = [Boolean(values[i]) ? 1 : -0.5]
    for (j = 0; j < values2.length; j++) {
      if (values[i] === values2[j]) {
        row.push(1.)
      } else if (values[i] == values2[j]) {
        row.push(0.5)
      } else if (values[i] == values[j]) {
        row.push(0)
      } else if (values[i] != values2[j]) {
        // row.push(-1)
        row.push(-0.5)  // purely for graphical reasons
      } else {
        row.push(0.)
      }
    }
    rows.push(row)
  }

  return {labels: ["Boolean(x)"].concat(values.map(stringify)), rows: rows}
}

const stringify = x => {
  if (typeof(x) === 'number' || x === undefined) {
    return String(x)
    // otherwise it won't work for:
    // NaN, Infinity, undefined
  } else {
    return JSON.stringify(x)
  }
}


export default CorrelationChartContainer
