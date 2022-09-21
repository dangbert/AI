import React, { useCallback, useState } from 'react';
import SafestAreaView from './lib/SafestAreaView';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  Button,
  Linking,
  Platform,
  Alert,
} from 'react-native';

import Agent, { Point } from './algo/Agent';
import {
  ExperimentConfig,
  ExperimentStats,
  runExperiment,
  examplePoints,
} from './algo/salesman';

const safeParse = (text: string, callback: (val: number) => void) => {
  try {
    const num = parseInt(text);
    callback(num);
  } catch (e) {}
};

interface SalesmanProps {}

const Salesman: React.FC<SalesmanProps> = ({}) => {
  const [points, setPoints] = useState<Point[]>(examplePoints);

  // config
  //   TODO: use ExperimentConfig
  const [maxGenerations, setMaxGenerations] = useState(30);
  const [targetPopSize, setTargetPopSize] = useState(40);
  const [numChildren, setNumChildren] = useState(20);
  const [probMutation, setProbMutation] = useState(0.05);

  // stats
  const [stats, setStats] = useState<ExperimentStats | undefined>(undefined);
  //const [stats, setStats] = useState<ExperimentStats | undefined>({
  //  running: true,
  //  curGeneration: 555,
  //  fitStats: {
  //    max: 66,
  //    avg: 66,
  //    min: 66,
  //  },
  //  population: [],
  //  bestAgent: new Agent(2),
  //});

  const running = stats?.running || false;

  //const statusCallback = useCallback(
  //  () => (stats: ExperimentStats) => {
  //    console.log('*****in satusCallback!*****');
  //    setStats(stats);
  //  },
  //  []
  //);

  const statusCallback = () => (stats: ExperimentStats) => {
    console.log('*****in statusCallback!*****');
    setStats(stats);
  };

  return (
    <SafestAreaView style={styles.container}>
      {/* experiment config: */}
      <View style={styles.centeredContent}>
        <View style={styles.row}>
          <Text style={styles.label}>Generations:</Text>
          <TextInput
            onChangeText={(val) => safeParse(val, setMaxGenerations)}
            value={maxGenerations.toString()}
          />
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Population Size:</Text>
          <TextInput
            onChangeText={(val) => safeParse(val, setTargetPopSize)}
            value={targetPopSize.toString()}
          />
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>Children Per Generation:</Text>
          <TextInput
            onChangeText={(val) => safeParse(val, setNumChildren)}
            value={numChildren.toString()}
          />
        </View>

        <View style={styles.row}>
          <Text style={styles.label}>P(mutation):</Text>
          <TextInput
            onChangeText={(val) => safeParse(val, setProbMutation)}
            value={probMutation.toString()}
          />
        </View>

        <View
          style={[
            styles.row,
            {
              marginTop: 24,
              marginBottom: 24,
              width: '80%',
              borderBottomWidth: 3,
            },
          ]}
        />
      </View>

      {/* stats / controls */}
      <View style={styles.centeredContent}>
        <>
          <View style={styles.row}>
            <Button
              title={running ? 'Pause' : 'Start'}
              onPress={async () => {
                const config: ExperimentConfig = {
                  maxGenerations,
                  targetPopSize,
                  probMutation,
                };
                console.log('starting experiment');
                runExperiment(points, config, statusCallback);
              }}
            />
          </View>

          {stats === undefined
            ? null
            : (() => {
                const { curGeneration, fitStats, population, bestAgent } =
                  stats;

                return (
                  <>
                    <View style={styles.row}>
                      <Text style={styles.label}>
                        Cur Generations: {curGeneration}
                      </Text>
                    </View>

                    <View style={styles.row}>
                      <Text>Cur population size: {population.length}</Text>
                    </View>

                    <View style={styles.row}>
                      <Text>
                        Fitness: {fitStats.max.toFixed(3)} max,{' '}
                        {fitStats.avg.toFixed(3)} avg, {fitStats.min.toFixed(3)}{' '}
                        min
                      </Text>
                    </View>

                    <View style={styles.row}>
                      <Button
                        title="View Best Solution"
                        onPress={() => {
                          // https://stackoverflow.com/a/48006762
                          // TODO: try https://github.com/includable/react-native-map-link
                          // TODO: don't hardcode
                          const rawUrl =
                            'https://www.google.com/maps/dir/52.35578270872273,4.955728233775735/52.36981757482324,4.880850114081587/52.358066655876875,4.868508923865922/52.33974766878963,4.842427613789914/52.33376991193947,4.865569696293274/52.33137852041053,4.868057053740658/52.32144690826629,4.872101596511191/52.31184849364095,4.84772881995548/52.30112397858448,4.844430244769097';
                          // const scheme = Platform.select({
                          // ios: 'maps:0,0?q=',
                          // android: 'geo:0,0?q=',
                          // });
                          Linking.openURL(bestAgent.toUrl(points)).catch(
                            (err) => Alert.alert(err)
                          );
                        }}
                      />
                    </View>
                  </>
                );
              })()}
        </>
      </View>
    </SafestAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#4ECDC4',
    fontSize: 16,
  },
  centeredContent: {
    marginTop: 12,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 4,
  },
  label: {
    paddingRight: 12,
  },
});

export default Salesman;
