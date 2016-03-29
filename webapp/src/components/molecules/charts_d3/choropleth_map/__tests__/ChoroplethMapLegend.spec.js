import { expect } from 'chai';
import _ from 'lodash';
import d3 from 'd3';
import MapLegend from '../ChoroplethMapLegend.js';

describe(__filename, () => {
  describe('ChoroplethMapLegend', () => {
    var mapLegendInstance;
    const goodBound = 0.9;
    const badBound = 0.8;
    var options;
    beforeEach(() => {
      mapLegendInstance = new MapLegend();
      options = {
        ticks: {
          goodBound: goodBound, badBound: badBound
        },
        data_format: 'pct',
        reversed: false
      };
      mapLegendInstance.DEFAULTS = {
        aspect: 1,
        domain: _.noop,
        margin: {
          top: 0,
          right: 0,
          bottom: 0,
          left: 0
        },
        data_format: 'pct',
        color: 'CURRENTLY NOT USED.',
        onClick: _.noop,
        yFormat: d => d3.format(Math.abs(d) < 1 ? '.4f' : 'n')(d),
        name: _.property('properties.name'),
        maxBubbleValue: 5000,
        maxBubbleRadius: 25,
        bubbleLegendRatio: [0.1, 0.5, 1]
      };
    });

    it('instantiates object with the proper class', () => {
      expect(mapLegendInstance).to.be.an.instanceof(MapLegend);
    });
    it('is extensible', () => {
      expect(mapLegendInstance).to.be.extensible;
    });
    it('has existing method', () => {
      expect(mapLegendInstance).to.respondTo('update');
      expect(mapLegendInstance).to.respondTo('initialize');
      expect(mapLegendInstance).to.respondTo('buildTicksFromBounds');
    });
    describe('#defaults', () => {
      it('has attribute', () => {
        expect(mapLegendInstance.defaults).to.exist;
      });
      it('has specific keys', () => {
        expect(mapLegendInstance.defaults).include.keys(
          'aspect',
          'domain',
          'margin',
          'data_format',
          'color',
          'onClick',
          'yFormat',
          'name',
          'maxBubbleValue',
          'maxBubbleRadius',
          'bubbleLegendRatio'
        );
        expect(mapLegendInstance.defaults.margin).keys('top', 'right', 'bottom', 'left');
      });
    });
    describe('#initialize()', () => {
      it('requires correct number of parameters', () => {
        expect(mapLegendInstance.initialize.length).to.be.eq(3);
      });
    });
    describe('#update()', () => {
      it('requires correct number of parameters', () => {
        expect(mapLegendInstance.update.length).to.be.eq(2);
      });
    });
    describe('#buildTicksFromBounds()', () => {
      it('requires correct number of parameters', () => {
        expect(mapLegendInstance.buildTicksFromBounds.length).to.be.eq(1);
      });
      context('percentage data format indicator', ()=>{
        context('bad bound less than good bound', () => {
          beforeEach(() => {
            options.data_format = 'pct';
            options.ticks.goodBound = goodBound;
            options.ticks.badBound = badBound;
            options.ticks.reversed = false;
          });
          it('returns legendTicks of bad range, middle range, good range', () => {
            var legendTicks = [`0%-${options.ticks.badBound*100}%`, `${options.ticks.badBound*100}%-${options.ticks.goodBound*100}%`,`${options.ticks.goodBound*100}%-100%`];
            expect(mapLegendInstance.buildTicksFromBounds(options)).to.have.members(legendTicks);
          });
          it('returns legendTicks of bad range, middle range, good range in correct order', () => {
            var legendTicks = [`0%-${options.ticks.badBound*100}%`, `${options.ticks.badBound*100}%-${options.ticks.goodBound*100}%`,`${options.ticks.goodBound*100}%-100%`];
            const ticks = mapLegendInstance.buildTicksFromBounds(options);
            expect(ticks[0]).to.be.eq(legendTicks[2]);
            expect(ticks[1]).to.be.eq(legendTicks[1]);
            expect(ticks[2]).to.be.eq(legendTicks[0]);
          });
        });
        context('bad bound greater than good bound', () => {
          beforeEach(() => {
            options.data_format = 'pct';
            options.ticks.goodBound = goodBound;
            options.ticks.badBound = badBound;
            options.ticks.reversed = true;
          });
          it('returns legendTicks of good range, middle range, bad range', () => {
            var legendTicks = [`${options.ticks.goodBound*100}%-100%`, `${options.ticks.badBound*100}%-${options.ticks.goodBound*100}%`, `0%-${options.ticks.badBound*100}%`];
            const ticks = mapLegendInstance.buildTicksFromBounds(options);
            expect(ticks).to.have.members(legendTicks);
          });
          it('returns legendTicks of good range, middle range, bad range in correct order', () => {
            var legendTicks = [`0%-${options.ticks.badBound*100}%`, `${options.ticks.badBound*100}%-${options.ticks.goodBound*100}%`,`${options.ticks.goodBound*100}%-100%`];
            const ticks = mapLegendInstance.buildTicksFromBounds(options);
            expect(ticks[0]).to.be.eq(legendTicks[0]);
            expect(ticks[1]).to.be.eq(legendTicks[1]);
            expect(ticks[2]).to.be.eq(legendTicks[2]);
          });
        });
      });
      context('boolean data format indicator', ()=>{
        context('bad bound less than good bound for indicator', () => {
          beforeEach(() => {
            options.data_format = 'bool';
            options.ticks.goodBound = goodBound;
            options.ticks.badBound = badBound;
            options.ticks.reversed = false;
          });
          it('returns legendTicks of \"Yes, No\"', () => {
            expect(mapLegendInstance.buildTicksFromBounds(options)).to.have.members(['Yes', 'No']);
          });
          it('returns legendTicks of \"Yes, No\" in correct order', () => {
            expect(mapLegendInstance.buildTicksFromBounds(options)[0]).to.be.eq('Yes');
            expect(mapLegendInstance.buildTicksFromBounds(options)[1]).to.be.eq('No');
          });
        });
      });
      context('integer data format indicator', ()=>{
        context('bad bound less than good bound', () => {
          beforeEach(() => {
            options.data_format = 'int';
            options.ticks.goodBound = 2;
            options.ticks.badBound = 1;
            options.ticks.reversed = false;
          });
          it('returns legendTicks of bad range, middle range, good range', () => {
            var legendTicks = [`0-${options.ticks.badBound}`, `${options.ticks.badBound}-${options.ticks.goodBound}`,`${options.ticks.goodBound}+`];
            expect(mapLegendInstance.buildTicksFromBounds(options)).to.have.members(legendTicks);
          });
          it('returns legendTicks of bad range, middle range, good range in correct order', () => {
            var legendTicks = [`0-${options.ticks.badBound}`, `${options.ticks.badBound}-${options.ticks.goodBound}`,`${options.ticks.goodBound}+`];
            const ticks = mapLegendInstance.buildTicksFromBounds(options);
            expect(ticks[0]).to.be.eq(legendTicks[2]);
            expect(ticks[1]).to.be.eq(legendTicks[1]);
            expect(ticks[2]).to.be.eq(legendTicks[0]);
          });
        });
        context('bad bound greater than good bound', () => {
          beforeEach(() => {
            options.data_format = 'int';
            options.ticks.goodBound = 1;
            options.ticks.badBound = 2;
            options.ticks.reversed = true;
          });
          it('returns legendTicks of good range, middle range, bad range', () => {
            var legendTicks = [`0-${options.ticks.goodBound}`, `${options.ticks.goodBound}-${options.ticks.badBound}`, `${options.ticks.badBound}+`];
            var temp = options.ticks.badBound;
            options.ticks.badBound = options.ticks.goodBound;
            options.ticks.goodBound = temp;
            expect(mapLegendInstance.buildTicksFromBounds(options)).to.have.members(legendTicks);
          });
          it('returns legendTicks of good range, middle range, bad range in correct order', () => {
            var legendTicks = [`${options.ticks.badBound}+`, `${options.ticks.goodBound}-${options.ticks.badBound}`,`0-${options.ticks.goodBound}`];
            var temp = options.ticks.badBound;
            options.ticks.badBound = options.ticks.goodBound;
            options.ticks.goodBound = temp;
            const ticks = mapLegendInstance.buildTicksFromBounds(options);
            expect(ticks[0]).to.be.eq(legendTicks[2]);
            expect(ticks[1]).to.be.eq(legendTicks[1]);
            expect(ticks[2]).to.be.eq(legendTicks[0]);
          });
        });
      });
    });
  });
});