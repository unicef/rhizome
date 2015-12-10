import { expect } from 'chai'

import format from '../format.js'

describe(__filename, () => {
  context('general format', () => {
    it('should format mantissa correctly', () => {
      const result = format.general(3.1415926)
      expect(result).to.eq('3.1416')
    })
    it('should format integer correctly', () => {
      const result = format.general(356)
      expect(result).to.eq('356')
    })
  })
  context('time axis format', () => {
    it('should format to month if not January', () => {
      const result = format.timeAxis(new Date('2001-10-01'))
      expect(result).to.eq('Oct')
    })
    it('should format to year if January', () => {
      const result = format.timeAxis(new Date('2001-01-01'))
      expect(result).to.eq('2001')
    })
  })
})
