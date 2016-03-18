import { expect } from 'chai';
import _ from 'lodash';
import ChoroplethMap from '../ChoroplethMap.js';
var lodash = require('lodash');

describe(__filename, () => {
  context('ChoroplethMap', () => {
    var choroplethMapInstance;
    beforeEach(() => {
      choroplethMapInstance = undefined;
      choroplethMapInstance = new ChoroplethMap();
    });

    it('should instantiate object', () => {
      expect(choroplethMapInstance).to.be.an.instanceof(ChoroplethMap);
    });
    it('should be extensible', () => {
      expect(choroplethMapInstance).to.be.extensible;
    });
    context('#defaults', () => {
      it('should have attribute', () => {
        expect(choroplethMapInstance.defaults).to.exist;
      });
      it('should have these specific keys', () => {
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
      });
    });
    context('#initialize()', () => {
      it('should have required methods', () => {
        expect(choroplethMapInstance).to.respondTo('initialize');
      });
      it('should require correct number of parameters', () => {
        expect(choroplethMapInstance.initialize.length).to.be.eq(3);
      });
    });
    context('#update()', () => {
      it('should have required methods', () => {
        expect(choroplethMapInstance).to.respondTo('update');
      });
      it('should require correct number of parameters', () => {
        expect(choroplethMapInstance.update.length).to.be.eq(2);
      });
    });
    describe('#getColor()', () => {
      const GREEN = '#83F5A2';
      const YELLOW = '#FFED89';
      const RED = '#FF9489';
      const goodBound = 0.9;
      const badBound = 0.8;
      var counter = 0;
      beforeEach(() => {
        var domain = [badBound, goodBound];
        choroplethMapInstance._options = {
          domain: _.constant(domain),
          color: [RED, YELLOW, GREEN]
        };
      });
      context('good bound greater than bad bound',() => {
        it('should have required methods', () => {
          expect(choroplethMapInstance).to.respondTo('getColor');
        });
        it('should require correct number of parameters', () => {
          expect(choroplethMapInstance.getColor.length).to.be.eq(1);
        });
        it('should return green for good bound indicator', () => {
          const goodIndicator = 0.95;
          expect(choroplethMapInstance.getColor(goodIndicator)).to.be.eq(GREEN);
        });
        it('should ONLY return green for good bound indicator', () => {
          const goodIndicator = 0.95;
          expect(choroplethMapInstance.getColor(goodIndicator)).to.not.be.eq(YELLOW);
          expect(choroplethMapInstance.getColor(goodIndicator)).to.not.be.eq(RED);
        });
        it('should return red for bad bound indicator', () => {
          const badIndicator = 0.79;
          expect(choroplethMapInstance.getColor(badIndicator)).to.be.eq(RED);
        });
        it('should ONLY return red for bad bound indicator', () => {
          const badIndicator = 0.79;
          expect(choroplethMapInstance.getColor(badIndicator)).to.not.be.eq(YELLOW);
          expect(choroplethMapInstance.getColor(badIndicator)).to.not.be.eq(GREEN);
        });
        it('should return yellow for bad bound indicator', () => {
          const okIndicator = 0.85;
          expect(choroplethMapInstance.getColor(okIndicator)).to.be.eq(YELLOW);
        });
        it('should ONLY return yellow for bad bound indicator', () => {
          const okIndicator = 0.85;
          expect(choroplethMapInstance.getColor(okIndicator)).to.not.be.eq(RED);
          expect(choroplethMapInstance.getColor(okIndicator)).to.not.be.eq(GREEN);
        });
      });
      context('if good and bad bounds are reversed', () => {
        beforeEach(() => {
          choroplethMapInstance._options.domain = _.constant(choroplethMapInstance._options.domain().reverse());
        });
        it('should return green for good bound indicator', () => {
          const goodIndicator = 0.79;
          expect(choroplethMapInstance.getColor(goodIndicator)).to.be.eq(GREEN);
        });
        it('should ONLY return green for good bound indicator', () => {
          const goodIndicator = 0.79;
          expect(choroplethMapInstance.getColor(goodIndicator)).to.not.be.eq(YELLOW);
          expect(choroplethMapInstance.getColor(goodIndicator)).to.not.be.eq(RED);
        });
        it('should return red for bad bound indicator', () => {
          const badIndicator = 0.95;
          expect(choroplethMapInstance.getColor(badIndicator)).to.be.eq(RED);
        });
        it('should ONLY return red for bad bound indicator', () => {
          const badIndicator = 0.95;
          expect(choroplethMapInstance.getColor(badIndicator)).to.not.be.eq(YELLOW);
          expect(choroplethMapInstance.getColor(badIndicator)).to.not.be.eq(GREEN);
        });
        it('should return yellow for bad bound indicator', () => {
          const okIndicator = 0.85;
          expect(choroplethMapInstance.getColor(okIndicator)).to.be.eq(YELLOW);
        });
        it('should ONLY return yellow for bad bound indicator', () => {
          const okIndicator = 0.85;
          expect(choroplethMapInstance.getColor(okIndicator)).to.not.be.eq(RED);
          expect(choroplethMapInstance.getColor(okIndicator)).to.not.be.eq(GREEN);
        });
      });
    });
  });
});