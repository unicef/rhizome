import { expect } from 'chai'
import React from 'react'

import MenuItem from '../MenuItem.jsx'

describe(__filename, () => {
  context('static method fromArray', () => {
    it('should return expected JSX', () => {
      let arr = [
        {
          'value': 'alpha'
        },
        {
          'value': 'beta'
        }
      ]
      expect(MenuItem.fromArray(arr, 'sendValue', 1)).to.deep.equal(
        [
          (<MenuItem
            key='alpha'
            depth={1}
            value='alpha'
            sendValue='sendValue'>
          </MenuItem>),
          (<MenuItem
            key='beta'
            depth={1}
            value='beta'
            sendValue='sendValue'>
          </MenuItem>)
        ]
      )
    })
  })
})
