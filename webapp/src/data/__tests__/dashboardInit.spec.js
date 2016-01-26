import _ from 'lodash'
import { expect } from 'chai'

import { childOf } from '../dashboardInit.js'
import { inChart } from '../dashboardInit.js'
import { choropleth } from '../dashboardInit.js'
import { getFacet } from '../dashboardInit.js'
import { series } from '../dashboardInit.js'

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

  context('get choropleth data', () => {
    let campaign = { id: 1 }
    let data = [
      {
        campaign: { id: 1 },
        location: { id: 1 },
        indicator: { id: 1 },
        value: 0.3
      },
      {
        campaign: { id: 2 },
        location: { id: 1 },
        indicator: { id: 1 },
        value: 0.5
      }
    ]

    context('should generate chropleth features when original features matches data', () => {
      let originalFeatures = [
        {
          properties: { location_id: 1 }
        }
      ]
      let expectedFeatures = [
        {
          properties:
            {
              location_id: 1,
              1: 0.3
            }
        }
      ]
      let actualFeatures = choropleth(null, data, campaign, originalFeatures)
      expect(actualFeatures).to.eql(expectedFeatures)
    })
    context('should not generate chropleth features when original features donnot match data', () => {
      let originalFeatures = [
        {
          properties: { location_id: 3 }
        }
      ]
      let actualFeatures = choropleth(null, data, campaign, originalFeatures)
      expect(actualFeatures).to.eql(originalFeatures)
    })
  })

  context('getFacet', () => {
    context('should get path in data when path exists', () => {
      let datum = { name: 'test' }
      let path = 'name'
      expect(getFacet(datum, path)).to.eql('test')
    })
    context('should get first element in data when data has two layers', () => {
      let datum = {name: {short_name: 'test', name: 'test_indicator', title: 'ttt', id: '1'}}
      let path = 'name'
      expect(getFacet(datum, path)).to.eql('test')
    })
  })

  context('test for series method', () => {
    context('should get legal data', () => {
      let chart = { groupBy: 'location.name' }
      let legalDataA = {
        location: { id: 1, name: 'a' },
        indicator: { id: 1 },
        value: 1
      }
      let dataValueEqualsZero = {
        location: { id: 1, name: 'a' },
        indicator: { id: 2 },
        value: 0
      }
      let legalDataB = {
        location: { id: 2, name: 'b' },
        indicator: { id: 3 },
        value: 2
      }
      let originalData = [
        legalDataA,
        dataValueEqualsZero,
        legalDataB
      ]
      let expectedData = [
        {
          name: 'a',
          values: [legalDataA]
        },
        {
          name: 'b',
          values: [legalDataB]
        }
      ]
      console.log(series(chart, originalData), expectedData)
      expect(series(chart, originalData)).to.eql(expectedData)
    })
  })
})
