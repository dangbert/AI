export interface Point {
  x: number;
  y: number;
  name?: string;
}

export type Genome = number[]; // list of indices into array: Point[]

export default class Agent {
  _nextId: number = 0;
  id: number;
  genome: Genome;

  public constructor(problemSize: number = 0, genome?: Genome) {
    this.id = this._nextId;
    this._nextId += 1;

    problemSize = problemSize || genome.length || 0;

    if (genome === undefined) {
      // random genome
      this.genome = [...Array(problemSize).keys()];
      this.genome.sort((a, b) => Math.random() - 0.5);
    } else {
      this.genome = genome;
    }
  }

  public getFitness(points: Point[]): number {
    let fitness = 0;
    for (let i = 1; i < this.genome.length; i++) {
      // get distance from previous point
      fitness += Math.sqrt(
        Math.pow(points[i - 1].x - points[i].x, 2) +
          Math.pow(points[i - 1].y - points[i].y, 2)
      );
    }
    return fitness * 100; // scaling up for readability
  }

  /**
   * Given two agents, breed them using crossover
   */
  public static breed(a1: Agent, a2: Agent): Agent {
    // TODO
    const genome = Agent.crossover(a1.genome, a2.genome);
    return new Agent(genome.length, genome);
  }

  public static crossover(g1: Genome, g2: Genome): Genome {
    return g1; // TODO for now
  }
}
