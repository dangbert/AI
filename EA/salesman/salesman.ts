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
 * @param count number of Agents to select from pop to be parents.
 */
const selectParents = (count: number, pop: Agent[]): number[] => {
  const fitnessSum = _.sum(pop.map((a) => a.fitness));
  const pool = _.shuffle(pop);
  let parentIndices = [];
  const used = new Set<number>();

  let i = -1;
  while (parentIndices.length < count) {
    i = (i + 1) % pop.length;
    if (used.has(i)) continue;
    const prob = pool[i].fitness / fitnessSum;
    const val = _.random(0, 1, true);
    if (val <= prob) parentIndices.push(i);
  }
  parentIndices = parentIndices.slice(0, count);
  return parentIndices;
};

/**
 * Selects agents to breed (probability of reproducing based on relative fitness).
 * Breed untils we reach population of size tagetSize (or can't produce any more unique genomes).
 *
 * @param pop
 * @param targetSize
 */
const createChildren = (count: number, pop: Agent[]) => {
  const existingGenomes = new Set<string>(pop.map((a) => a.genome.join(',')));
  let children: Agent[] = [];
  const numChildren = count * 1.0;
  const maxAttempts = numChildren * 50; // max times to try to create new unqiue genomes
  let attempts = 0;
  while (children.length < numChildren && attempts < maxAttempts) {
    const parents = selectParents(2, pop).map((i) => pop[i]);
    /*
    console.log(
      `selected parents with Ids: ${
        parents[0].id
      } (fitness ${parents[0].fitness.toFixed(2)}), ${
        parents[1].id
      } (fitness ${parents[1].fitness.toFixed(2)})`
    );
    */
    let newChildren = Agent.breed(parents[0], parents[1]);
    // ensure no duplicates are added to population!
    for (const a of newChildren) {
      if (existingGenomes.has(a.genome.join(','))) continue;
      children = children.concat(newChildren);
      existingGenomes.add(a.genome.join(','));
    }
    attempts += 1;
  }
  children.forEach((c) => c.getFitness(points)); // compute fitness
  return children;
};

/**
 * Perform selection on population, returning a subset of the original population of targetSize members.
 * @param pop
 * @param targetSize
 * @returns
 */
const prunePopulation = (pop: Agent[], targetSize: number) => {
  const fitnessSum = _.sum(pop.map((a) => a.fitness));
  const used = new Set<number>();
  const newPop: Agent[] = [];

  let i = -1;
  while (newPop.length < targetSize) {
    i = (i + 1) % pop.length;
    if (used.has(i)) continue;
    const agent = pop[i];
    if (newPop.length >= targetSize) break;
    const prob = agent.fitness / fitnessSum;
    if (_.random(0, 1, true) <= prob) newPop.push(agent);
  }
  return newPop;
};

(async () => {
  const totalPoints = points.length;
  const targetPopSize = 20; // desired population size
  const maxGenerations = 100;

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

    // breed until we have doubled the population (or can't produce any more unique genomes)
    const children = createChildren(targetPopSize * 1.0, pop);
    pop = pop.concat(children);
    console.log(`grew population to size: ${pop.length}`);

    // TODO: mutate agents with chance of 0.1

    // select popSize agents to keep (probability of surviving based on relative fitness)
    pop = prunePopulation(pop, targetPopSize);
    console.log(`pruned population to size: ${pop.length}`);
  }
  console.log('done!');
  // TODO: write csv of stats to file!
})();
