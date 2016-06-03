import React from 'react'
import expect from 'expect'
import TestUtils from 'react-addons-test-utils'
import CampaignsPage from 'components/pages/campaigns/CampaignsPage'
import CampaignPage from 'components/pages/campaigns/CampaignPage'
import CampaignEditPage from 'components/pages/campaigns/CampaignEditPage'

describe('CampaignsPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<CampaignsPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('CampaignPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<CampaignPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})

describe('CampaignEditPage', () => {
  let renderer = TestUtils.createRenderer()
  renderer.render(<CampaignEditPage />)
  let output = renderer.getRenderOutput()

  it ('renders an div', () => {
    expect(output.type).toBe('div')
  })
})
