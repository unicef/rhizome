import { expect } from 'chai';
import ChoroplethMap from '../ChoroplethMap.js';
var lodash = require('lodash');

describe(__filename, () => {
  context('ChoroplethMap', () => {
    const choroplethMapInstance = new ChoroplethMap();
    it('should instantiate object', () => {
      expect(choroplethMapInstance).to.be.an.instanceof(ChoroplethMap);
    })
    it('should have \"defaults\" attribute', () => {
      expect(choroplethMapInstance.defaults).to.exist;
    })
    it('should have these specific defaults', () => {
      expect(choroplethMapInstance.defaults).include.keys(
        'aspect',
        'domain',
        'margin',
        'data_format', 'onClick',
        'value',
        'color',
        'xFormat',
        'name',
        'maxBubbleValue',
        'maxBubbleRadius',
        'bubbleLegendRatio',
        'indicatorName'
      );
      expect(choroplethMapInstance.defaults.margin).keys('top', 'right', 'bottom', 'left');
    })
    it('should be extensible', () => {
      expect(choroplethMapInstance).to.be.extensible;
    })
    it('should have required methods', () => {
      expect(choroplethMapInstance).to.respondTo('initialize');
      expect(choroplethMapInstance).to.respondTo('getColor');
      expect(choroplethMapInstance).to.respondTo('update');
    })
    it('should require correct number of parameters', () => {
      expect(choroplethMapInstance.initialize.length).to.be.eq(3)
      expect(choroplethMapInstance.update.length).to.be.eq(2)
      expect(choroplethMapInstance.getColor.length).to.be.eq(2)
    })
  })
})