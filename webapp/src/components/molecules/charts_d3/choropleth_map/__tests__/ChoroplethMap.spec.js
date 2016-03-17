import { expect } from 'chai'

import ChoroplethMap from '../ChoroplethMap.js'

describe(__filename, () => {
  context('ChoroplethMap', () => {
    const choroplethMap = new ChoroplethMap()
    it('should instantiate object', () => {
      expect(typeof choroplethMap).to.equal('object')
    })
    it('should be the correct object instance', () => {
      expect(choroplethMap.constructor.name).to.equal('ChoroplethMap')
    })
    it('has all required functions', () => {
      expect(choroplethMap.constructor.name).to.equal('ChoroplethMap')
    })
  })
})