import { expect } from 'chai'
import React from 'react'
import d3 from 'd3'
import _ from 'lodash'

import Performance from '../Performance.jsx'
import data from './data.json'

function series(values, name) {
  return {
    name: name,
    values: _.sortBy(values, _.result('campaign.start_date.getTime'))
  }
}

function jsonLog(json) {
  console.log(JSON.stringify(json))
}

describe.only(__filename, () => {
  context('missed children data inconsistent with d3', () => {
    it('should throw error', () => {
      let stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'));

      let missed = _(data.splice(10, 4))
        .groupBy('indicator.short_name')
        .map(series)
        .tap(jsonLog)
        .thru(stack)
        .value();
    })
  })
})
