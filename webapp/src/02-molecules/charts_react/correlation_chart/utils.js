import d3 from 'd3'

const scale = (label_col, label_row) => {
	return d3.scale.linear()
  .domain([0, d3.min([50, d3.max([label_col.length, label_row.length, 4])])])
  .range([0, parseFloat(d3.select('input#zoom')[0][0].value) * 600])
}

export default scale