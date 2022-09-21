import React from 'react';
import {
  SafeAreaView,
  ViewProps,
  StyleSheet,
  Platform,
  StatusBar,
} from 'react-native';

/**
 * SafeAreaView but automatically handles Android as well as IOS.
 * (Wrapper around SafeAreaView)
 */
export default function SafestAreaView(props: ViewProps) {
  //let style = {...styles.safeHeader, ...{ props.style || {}} };
  const { style, children } = props;

  return (
    <SafeAreaView
      {...props}
      style={Object.assign({}, styles.safeHeader, style)}
    >
      {children}
    </SafeAreaView>
  );
}
const styles = StyleSheet.create({
  safeHeader: {
    paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight : 0,
  },
});
