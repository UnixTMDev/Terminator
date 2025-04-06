from TTS.api import TTS
from pydub import AudioSegment
import simpleaudio as sa
import shutil


test_text = """The Market Gardener is a community-created melee weapon for the Soldier. It is an entrenching shovel with a tan wooden handle fastened with green metal.

The Market Gardener deals Critical hits to enemies whilst the wielder is rocket jumping (or otherwise airborne via explosion), but cannot randomly Crit. Compared to the default Shovel, the Market Gardener has a 20 percent slower swinging speed. """

def speak(text,modelname):
    try:
        shutil.rmtree(".tts.wav")
    except NotADirectoryError:
        pass
    # Init TTS with a model
    tts = TTS(model_name=modelname, progress_bar=False, gpu=True)

    # Generate speech
    audio_path = ".tts.wav"
    tts.tts_to_file(text=text, file_path=audio_path)

    # Play the file immediately
    audio = AudioSegment.from_wav(audio_path)
    play_obj = sa.play_buffer(audio.raw_data, num_channels=audio.channels, bytes_per_sample=audio.sample_width, sample_rate=audio.frame_rate)
    play_obj.wait_done()

    try:
        shutil.rmtree(".tts.wav")
    except NotADirectoryError:
        pass

#tts_models/en/vctk
#tts_models/en/ljspeech/tacotron2-DDC

if __name__ == "__main__":
    speak(test_text,"tts_models/en/ljspeech/tacotron2-DDC")