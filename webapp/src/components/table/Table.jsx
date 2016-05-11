import React, {Component, PropTypes} from 'react'

class Table extends Component {
  renderCells = function (content) {
    const props = this.props
    return (
      <td>{content}</td>
    )
  }

  renderHeaderRow = function () {
    return (
      <tr></tr>
    )
  }

  renderRows = function () {
    const props = this.props
    return (
      <tr>{this.renderCells()}</tr>
    )
  }

  render = function () {
    return (
      <table>
        <thead>
          { this.renderHeaderRow() }
        </thead>
        { this.renderRows() }
      </table>
    )
  }
}

export default Table
