import React from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import { Audio } from 'expo-av';
import {Buffer} from 'buffer';


export default function App() {
  const [recording, setRecording] = React.useState();
  const [recordings, setRecordings] = React.useState([]);
  // const [soundObject, setSoundObject] = useState<Audio.Sound | null>(null);

  async function startRecording() {
    try {
      const perm = await Audio.requestPermissionsAsync();
      if (perm.status === "granted") {
        await Audio.setAudioModeAsync({
          allowsRecordingIOS: true,
          playsInSilentModeIOS: true,
        });
        const { recording } = await Audio.Recording.createAsync(Audio.RECORDING_OPTIONS_PRESET_HIGH_QUALITY);
        setRecording(recording);
      }
    } catch (err) {}
  }

  // applyAudioGain = (audioChunk, gain: number) => {
  //   const float32Array = new Float32Array(audioChunk);
  //   for (let i = 0; i < float32Array.length; i++) {
  //     float32Array[i] *= gain;
  //     // float32Array[i] = 0;
  //   }
  //   return Buffer.from(float32Array.buffer);
  // };

  async function stopRecording() {
    setRecording(undefined);

    await recording.stopAndUnloadAsync();
    let allRecordings = [...recordings];
    const { sound, status } = await recording.createNewLoadedSoundAsync();
    allRecordings.push({
      sound: sound,
      duration: getDurationFormatted(status.durationMillis),
      file: recording.getURI()
    });
    console.log(recording.getURI());
    setRecordings(allRecordings);
  }

  function getDurationFormatted(milliseconds) {
    const minutes = milliseconds / 1000 / 60;
    const seconds = Math.round((minutes - Math.floor(minutes)) * 60);
    return seconds < 10 ? `${Math.floor(minutes)}:0${seconds}` : `${Math.floor(minutes)}:${seconds}`
  }

  function getRecordingLines() {

    // const [sound, setSound] = useState();

    // async function playSound() {
    //   console.log('Loading Sound');
    //   const { sound } = await Audio.Sound.createAsync(
    //     require(recording.getURI()));
    //   setSound(applyAudioGain(sound, 2.0));

    //   console.log('Playing Sound');
    //   await sound.playAsync();
    // }

    // useEffect(() => {
    //   return sound
    //     ? () => {
    //         console.log('Unloading Sound');
    //         sound.unloadAsync();
    //       }
    //     : undefined;
    // }, [sound]);

    
    return recordings.map((recordingLine, index) => {
      return (
        <View key={index} style={styles.row}>
          <Text style={styles.fill}>
            Recording #{index + 1} | {recordingLine.duration}
          </Text>
          <Button onPress={() => recordingLine.sound.replayAsync()} title="Play"></Button>
        </View>
      );
    });
  }

  function clearRecordings() {
    setRecordings([])
  }

  return (
    <View style={styles.container}>
      <Button title={recording ? 'Stop Recording' : 'Start Recording'} onPress={recording ? stopRecording : startRecording} />
      {getRecordingLines()}
      <Button title={recordings.length > 0 ? 'Clear Recordings' : ''} onPress={clearRecordings} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    margin: 15
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginLeft: 10,
    marginRight: 40,
    // padding: 15

  },
  fill: {
    flex: 1,
    margin: 15
  }
});
