import Agent, { Point } from './Agent.js';
import _ from 'lodash';

const points: Point[] = [
  {
    x: 52.33376991193947,
    y: 4.865569696293274,
    name: 'VU',
  },
  {
    x: 52.32144690826629,
    y: 4.872101596511191,
    name: 'Uilenstede 48',
  },
  {
    x: 52.33974766878963,
    y: 4.842427613789914,
    name: 'Be Boulder',
  },
  {
    x: 52.358066655876875,
    y: 4.868508923865922,
    name: 'Vondel Park',
  },
  {
    x: 52.31184849364095,
    y: 4.84772881995548,
    name: 'Lidl',
  },
  {
    x: 52.33137852041053,
    y: 4.868057053740658,
    name: 'Free Wheely',
  },
  {
    x: 52.36981757482324,
    y: 4.880850114081587,
    name: 'Amsterdam Language Cafe',
  },
  {
    x: 52.30112397858448,
    y: 4.844430244769097,
    name: 'Municipality Amstelveen',
  },
  {
    x: 52.35578270872273,
    y: 4.955728233775735,
    name: 'UVA',
  },
];

/**
 * return array of indices of parents selected randomly from population based on relative fitness.
 */
const selectParents = (
  count: number,
  pop: Agent[],
  maxFitness: number
): number[] => {
  const pool = _.shuffle(pop);
  const parentIndices = [];
  const used = new Set<number>();

  while (parentIndices.length < count) {
    for (let i = 0; i < pool.length; i++) {
      if (used.has(i)) continue;
      const prob = pool[i].fitness / maxFitness;
      if (_.random(0, 1, true) <= prob) parentIndices.push(i);
    }
  }
  parentIndices.slice(0, count);
  return parentIndices;
};

const prunePopulation = (
  pop: Agent[],
  maxFitness: number,
  targetSize: number
) => {
  const newPop = [];
  for (const agent of pop) {
    if (newPop.length >= targetSize) break;
    const prob = agent.fitness / maxFitness;
    if (_.random(0, 1, true) <= prob) newPop.push(agent);
  }
  return newPop;
};

(async () => {
  const totalPoints = points.length;
  const targetPopSize = 20; // desired population size
  const maxGenerations = 20;

  //let population: Agent[] = []; // = new Array(popSize).fill(new Agent(totalPoints));
  let pop: Agent[] = []; // = new Array(targetPopSize).fill(new Agent(totalPoints));
  for (let i = 0; i < targetPopSize; i++) {
    pop.push(new Agent(totalPoints));
  }

  console.log(`starting generations... (totalPoints = ${totalPoints})`);
  for (let n = 0; n < maxGenerations; n++) {
    pop.sort((a, b) => b.fitness - a.fitness); // sort highest -> lowest

    let fitnesses = pop.map((agent) => agent.getFitness(points));
    const avgFitness = _.mean(fitnesses);
    const minFitness = _.min(fitnesses);
    const maxFitness = _.max(fitnesses);

    // report stats
    console.log(
      `\ngeneration: ${n},\tpop size: ${
        pop.length
      }, fitness: avg ${avgFitness.toFixed(2)}, max ${maxFitness.toFixed(
        2
      )}, min ${minFitness.toFixed(2)}`
    );

    pop = _.shuffle(pop);

    // select agents to breed (probability of reproducing based on relative fitness)
    // breed until we have doubled the population
    while (pop.length < targetPopSize * 2) {
      const parents = selectParents(2, pop, maxFitness).map((i) => pop[i]);
      //pop = pop.concat(Agent.crossover(parents[0], parents[1]).map(g => new Agent(g.length, g))):;
      const children = Agent.breed(parents[0], parents[1]);
      pop = pop.concat(children);
    }
    console.log(`grew population to size: ${pop.length}`);

    // TODO: later mutate agents with chance of 0.1

    // select popSize agents to keep (probability of surviving based on relative fitness)
    pop = prunePopulation(pop, maxFitness, targetPopSize);
    console.log(`pruned population to size: ${pop.length}`);
  }
})();
