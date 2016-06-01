import { expect } from 'chai'

import color from '../color.js'

const categories = ['alpha', 'bravo', 'charlie', 'delta', 'echo']

describe(__filename, () => {
  context('colour map', () => {
    it('should map colour with categories more than palette colours', () => {
      const palette = ['red', 'orange', 'yellow']
      const result = categories.map(category => {
        return color.map(categories, palette)(category)
      })
      expect(result).to.deep.eq(['red', 'orange', 'yellow', 'red', 'orange'])
    })
    it('should map colour with categories less than palette colours', () => {
      const palette = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']
      const result = categories.map(category => {
        return color.map(categories, palette)(category)
      })
      expect(result).to.deep.eq(['red', 'orange', 'yellow', 'green', 'cyan'])
    })
    it('should map colour using default palette', () => {
      const result = categories.map(category => {
        return color.map(categories)(category)
      })
      expect(result).to.deep.eq(['#334B61', '#222222', '#387EA3', '#436380', '#6493A6'])
    })
  })
  context('colour scale', () => {
    it('should expand palette averagely to categories', () => {
      const palette = ['red', 'purple']
      const result = categories.map(category => {
        return color.scale(categories, palette)(category)
      })
      expect(result).to.deep.eq(['#ff0000', '#df0020', '#c00040', '#a00060', '#800080'])
    })
    it('only first and last colour in palette should affect', () => {
      const palette = ['red', 'green', 'purple']
      const result = categories.map(category => {
        return color.scale(categories, palette)(category)
      })
      expect(result).to.deep.eq(['#ff0000', '#df0020', '#c00040', '#a00060', '#800080'])
    })
    it('should scale colour using default palette', () => {
      const result = categories.map(category => {
        return color.scale(categories)(category)
      })
      expect(result).to.deep.eq(['#377ea4', '#5793b0', '#77a7bc', '#96bcc8', '#b6d0d4'])
    })
  })
})
