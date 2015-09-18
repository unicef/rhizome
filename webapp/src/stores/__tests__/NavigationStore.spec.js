import { expect } from 'chai'
import _ from 'lodash'

import NavigationStore from '../NavigationStore.js'

describe(__filename, () => {
  context('filtering available locations', () => {
    it('should filter available locations from office id', () => {
      const locations = _([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        },
        {
          'location_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 1
      }
      let availablelocations = NavigationStore._filterlocations(dashboard, locations)
      expect(availablelocations.value()).to.deep.equal([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        }
      ])
    }),

    it('should not filter if not have match office id', () => {
      const locations = _([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        },
        {
          'location_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 2
      }
      let availablelocations = NavigationStore._filterlocations(dashboard, locations)
      expect(availablelocations.value()).to.deep.equal([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        },
        {
          'location_id': 2,
          'office_id': 0
        }
      ])
    })

    it('should return original location if default office id not valid', () => {
      const locations = _([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        },
        {
          'location_id': 2,
          'office_id': 0
        }
      ])
      const dashboard = {
        'default_office': 'not-number'
      }
      let availablelocations = NavigationStore._filterlocations(dashboard, locations)
      expect(availablelocations.value()).to.deep.equal([
        {
          'location_id': 0,
          'office_id': 1
        },
        {
          'location_id': 1,
          'office_id': 1
        },
        {
          'location_id': 2,
          'office_id': 0
        }
      ])
    })
  })
})
