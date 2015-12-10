import { expect } from 'chai'

import data from '../data.js'

describe(__filename, () => {
  context('rename', () => {
    it('should rename object key', () => {
      const obj = { a: 1, b: 2, c: 3 }
      const mapping = { b: 'd' }
      const expected = { a: 1, d: 2, c: 3 }
      expect(data.rename(obj, mapping)).to.deep.eq(expected)
    })
  })
  context('unpivot', () => {
    it('should unpivot object', () => {
      const obj = {
        objects: [
          {
            indicators: [
              { indicator: 'a', value: 'alpha' },
              { indicator: 'b', value: 'bravo' }
            ],
            y: 'yankee',
            z: 'zulu'
          },
          {
            indicators: [
              { indicator: 'c', value: 'charlie' },
              { indicator: 'd', value: 'delta' },
              { indicator: 'e', value: 'echo' }
            ],
            w: 'whisky',
            x: 'xray'
          }
        ]
      }
      const expected = [
        { indicator: 'b', value: 'bravo', y: 'yankee', z: 'zulu' },
        { indicator: 'a', value: 'alpha', y: 'yankee', z: 'zulu' },
        { indicator: 'e', value: 'echo', w: 'whisky', x: 'xray' },
        { indicator: 'd', value: 'delta', w: 'whisky', x: 'xray' },
        { indicator: 'c', value: 'charlie', w: 'whisky', x: 'xray' }
      ]
      expect(data.unpivot(obj)).to.deep.eq(expected)
    })
  })
})
