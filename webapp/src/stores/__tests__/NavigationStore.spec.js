import { expect } from 'chai'
import _ from 'lodash'

import NavigationStore from '../NavigationStore.js'

describe(__filename, () => {
  context('filtering available regions', () => {
    it('should filter available regions from office id', () => {
      const regions = _([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        },
        {
          'region_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 1
      }
      let availableRegions = NavigationStore._filterRegions(dashboard, regions)
      expect(availableRegions.value()).to.deep.equal([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        }
      ])
    }),

    it('should not filter if not have match office id', () => {
      const regions = _([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        },
        {
          'region_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 2
      }
      let availableRegions = NavigationStore._filterRegions(dashboard, regions)
      expect(availableRegions.value()).to.deep.equal([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        },
        {
          'region_id': 2,
          'office_id': 0
        }
      ])
    })

    it('should return original region if default office id not valid', () => {
      const regions = _([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        },
        {
          'region_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 'not-number'
      }
      let availableRegions = NavigationStore._filterRegions(dashboard, regions)
      expect(availableRegions.value()).to.deep.equal([
        {
          'region_id': 0,
          'office_id': 1
        },
        {
          'region_id': 1,
          'office_id': 1
        },
        {
          'region_id': 2,
          'office_id': 0
        }
      ])
    })
  })
})
