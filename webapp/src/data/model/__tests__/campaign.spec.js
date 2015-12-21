import { expect } from 'chai'

import campaign from '../campaign'

describe(__filename, () => {
  context('campaign', () => {
    it('should create campaign from empty', () => {
      expect(campaign()).to.deep.eq({
        id: null,
        created_at: null,
        start_date: null,
        end_date: null,
        name: null,
        slug: null,
        resource_uri: null
      })
    })
    it('should update new campaign', () => {
      const source = {
        id: 1,
        created_at: '2001-10-08',
        start_date: '2001-09-01',
        end_date: '2001-09-30',
        name: '2001-sep',
        slug: '2001-sep',
        resource_uri: '/'
      }
      expect(campaign(source)).to.deep.eq({
        id: 1,
        created_at: new Date('2001-10-08 00:00'),
        start_date: new Date('2001-09-01 00:00'),
        end_date: new Date('2001-09-30 00:00'),
        name: '2001-sep',
        slug: '2001-sep',
        resource_uri: '/'
      })
    })
  })
})
