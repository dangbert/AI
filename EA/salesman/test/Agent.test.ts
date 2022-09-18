import { describe, it } from 'mocha';
import { expect } from 'chai';
import Agent from '../Agent.js';

describe('class Agent', () => {
  describe('crossover()', () => {
    it('should work for simple example (no cycling required)', () => {});
    const p1 = new Agent(9);
    p1.genome = [0, 1, 2, 3, 4, 5, 6, 7, 8];

    const p2 = new Agent(9);
    p2.genome = [1, 0, 3, 2, 7, 8, 6, 4, 5];

    const splitPoint = 3;
    const children = Agent.crossover(p1.genome, p2.genome, splitPoint);

    expect(children[0]).to.eql([0, 1, 2, 3, 7, 8, 6, 4, 5]);
  });
});
