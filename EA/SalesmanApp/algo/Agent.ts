import _ from 'lodash';
export interface Point {
  x: number;
  y: number;
  name?: string;
}

export type Genome = number[]; // list of indices into array: Point[]

export default class Agent {
  static _nextId: number = 0;
  id: number;
  genome: Genome;
  fitness: number;

  public constructor(problemSize: number = 0, genome?: Genome) {
    this.id = Agent._nextId;
    Agent._nextId += 1;
    this.fitness = 0; // placeholder for now

    problemSize = genome !== undefined ? genome.length : problemSize;

    if (genome === undefined) {
      // random genome
      this.genome = [...Array(problemSize).keys()];
      this.genome = _.shuffle(this.genome);
    } else {
      this.genome = genome;
    }
  }

  /**
   * Return google maps URL exhibiting this Agent's solution.
   */
  public toUrl(points: Point[]) {
    // https://www.google.com/maps/dir/52.3557827,4.9557282/52.36981757482324,+4.880850114081587/The+North+Face+Amsterdam+-+Urban+Exploration,+Wolvenstraat,+Amsterdam/@52.3624346,4.8995718,14z/data=!3m1!4b1!4m13!4m12!1m0!1m3!2m2!1d4.8808501!2d52.3698176!1m5!1m1!1s0x47c60936979f07ab:0x8794e8984cdad60b!2m2!1d4.886154!2d52.3704014!3e0
    let url = 'https://www.google.com/maps/dir';
    this.genome.forEach((val) => {
      //console.log(`${points[val].x}, ${points[val].y}\t${points[val].name}`);
      url += `/${points[val].x},${points[val].y}`;
    });
    return url;
  }

  /**
   * larger fitness is better (all values will be negative).
   */
  public getFitness(points: Point[]): number {
    let fitness = 0;
    for (let i = 1; i < this.genome.length; i++) {
      // get distance from previous point
      fitness += Math.sqrt(
        Math.pow(points[this.genome[i - 1]].x - points[this.genome[i]].x, 2) +
          Math.pow(points[this.genome[i - 1]].y - points[this.genome[i]].y, 2)
      );
    }
    this.fitness = 1 / fitness; // taking inverse so larger fitness values are better
    return this.fitness;
  }

  /**
   * Given two agents, breed them using crossover
   */
  public static breed(a1: Agent, a2: Agent): Agent[] {
    // TODO
    const genomes = Agent.crossover(a1.genome, a2.genome);
    return genomes.map((g) => new Agent(g.length, g));
  }

  /**
   * Breed two genomes together to create two children.
   * A random index is selected at which to split the g1 sequence (from the start).
   * Then values from g2 (starting after the split index) are used to populate the rest of the new genome,
   * if a value is already in the new genome, its skipped and g2 is traversed in a circle until the final genome is the correct length.
   * (This process is done vice versa to produce a second child as well).
   */
  //public static crossover(g1: Genome, g2: Genome): Genome[] {
  public static crossover(
    g1: Genome,
    g2: Genome,
    splitIndex: number = -1
  ): Genome[] {
    const size = g1.length;
    // TODO: use a gaussian offset from the center index
    //  (bias crossover towards center index)
    if (splitIndex === -1) splitIndex = _.random(1, size, false);
    //console.log(`splitIndex = ${splitIndex}`);

    let children = [];
    for (let count = 0; count < 2; count++) {
      // parents
      const p1 = count ? g2 : g1;
      const p2 = count ? g1 : g2;

      const child: Genome = p1.slice(0, splitIndex + 1);
      //console.log('initial child genome:');
      //console.log(child);

      let used = new Set<number>(child); // already used values
      let i = splitIndex + 1;
      while (child.length < size) {
        //console.log(`i=${i}, considering adding ${p2[i]}`);
        if (!used.has(p2[i])) {
          //console.log(`  adding ${p2[i]} (i=${i})`);
          used.add(p2[i]);
          child.push(p2[i]);
        }
        i = (i + 1) % size;
      }
      children.push(child);
    }
    return children;
  }
}
