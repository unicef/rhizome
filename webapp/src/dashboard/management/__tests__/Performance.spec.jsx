import { expect } from 'chai'

import Performance from '../Performance.jsx'
import data from './data.json'

describe(__filename, () => {
  context('missed children data inconsistent with d3', () => {
    it('should not throw error', () => {
      expect(Performance.prototype.generateMissedChildrenChartData.bind(Performance, data)).to.not.throw(Error)
    })
  })
})
