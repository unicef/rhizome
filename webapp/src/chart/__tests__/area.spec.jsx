import { expect } from 'chai'

import Area from '../area.js'
import data from './data.json'

describe(__filename, () => {
  context('area data inconsistent with d3', () => {
    it('should not throw error', () => {
      expect(Area.prototype.generateChartData.bind(null, data)).to.not.throw(Error)
    })
  })
})
