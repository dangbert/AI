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

(async () => {
  //const genome: Genome = {};

  const totalPoints = points.length;

  const popSize = 20;

  const maxGenerations = 20;
  let population: Agent[] = []; // = new Array(popSize).fill(new Agent(totalPoints));

  for (let i = 0; i < popSize; i++) {
    population.push(new Agent(totalPoints));
  }

  for (let i = 0; i < maxGenerations; i++) {
    console.log(population[i].getFitness(points));
    console.log(population[i]);
  }

  for (let n = 0; n < maxGenerations; n++) {
    let fitnesses = population.map((agent) => agent.getFitness(points));
    const avgFitness = _.mean(fitnesses);
    const minFitness = _.min(fitnesses);
    const maxFitness = _.max(fitnesses);
    //const avgFitness =
    //  population.reduce<number>(
    //    (sum: number, cur: Agent) => sum + cur.getFitness(points),
    //    0
    //  ) / population.length;

    console.log(
      `\ngeneration: ${n},\tfitness: avg ${avgFitness.toFixed(
        2
      )}, max ${maxFitness.toFixed(2)}, min ${minFitness.toFixed(2)}`
    );
  }
})();
