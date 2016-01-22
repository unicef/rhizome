import _ from 'lodash'
import { expect } from 'chai'

import { childOf } from '../dashboardInit.js'
import { inChart } from '../dashboardInit.js'

describe(__filename, () => {
  context('child of', () => {
    context('child has no parent', () => {
      it('child has no parent_location_id', () => {
        let child = {
          not_parent: 1
        }
        let parent = {}
        expect(childOf(parent, child)).to.be.false
      })

      it('child has parent_location_id equals to parent.id', () => {
        let child = {
          parent_location_id: 1
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent_location_id not equal to parent.id', () => {
        let child = {
          parent_location_id: 1
        }
        let parent = {
          id: 2
        }
        expect(childOf(parent, child)).to.be.false
      })
    })

    context('child has parent', () => {
      it('child has parent.id equal to parent.id', () => {
        let child = {
          parent: {
            id: 1
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent.id not equal to parent.id, recursively call true case', () => {
        let child = {
          parent: {
            parent: {
              id: 1
            }
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.true
      })
      it('child has parent.id not equal to parent.id, recursively call false case', () => {
        let child = {
          parent: {
            parent: {
              no_parent: 2
            }
          }
        }
        let parent = {
          id: 1
        }
        expect(childOf(parent, child)).to.be.false
      })
    })
  })

  context('in chart', () => {
    let legalCampaign = { start_date: '2015-01-01' }
    let legalLocation = { id: 1, parent: { id: '1' } }
    let legalIndicator = { id: 1 }
    let legalDatum = {
      campaign: legalCampaign,
      location: legalLocation,
      indicator: legalIndicator
    }

    let illegalCampaign = { start_date: '2015-10-01' }
    let illegalLocation = { id: 2, parent: { id: 2 } }
    let illegalIndicator = { id: 2 }
    let illegalDatum = {
      campaign: illegalCampaign,
      location: illegalLocation,
      indicator: illegalIndicator
    }

    context('chart locations type is default', () => {
      it('should filter legal data with required conditions', () => {
        let data = [legalDatum]
        let indicators = [legalIndicator]
        let chart = {
          indicators: _.pluck(indicators, 'id')
        }
        var chartData = _.filter(data, _.partial(inChart, chart, legalCampaign, legalLocation))
        expect(chartData).to.eql([legalDatum])
      })
      it('should remove illegal data', () => {
        let data = [legalDatum, illegalDatum]
        let indicators = [legalIndicator, illegalIndicator]
        let chart = {
          indicators: _.pluck(indicators, 'id')
        }
        var chartData = _.filter(data, _.partial(inChart, chart, legalCampaign, legalLocation))
        expect(chartData).to.eql([legalDatum])
      })
    })
  })
})
