import requests
from .tts import TTS, TTSValidator
from mycroft.configuration import Configuration
import subprocess

_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/{}/stream"

class ElevenLabsTTS(TTS):
    def __init__(self, lang, config):
        super(ElevenLabsTTS, self).__init__(lang, config, ElevenLabsTTSValidator(self))
        tts_config = Configuration.get().get("tts", {})
        self.config = tts_config.get("elevenlabs", {})
        self.voice_id = self.config.get("voice_id")
        self.api_key = self.config.get("api_key")

    def get_tts(self, sentence, wav_file):
        url = _API_URL.format(self.voice_id)
        headers = {
            "Accept": "audio/wav",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": sentence,
            "voice_settings": {
                "stability": 0,
                "similarity_boost": 0
            }
        }
        response = requests.post(url, json=data, headers=headers, stream=True)
        
        raw_wav_file = wav_file + ".raw"
        with open(raw_wav_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # Re-encode the audio using ffmpeg-- required due to compatibility issues 
        subprocess.call(['ffmpeg', '-y', '-i', raw_wav_file, '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '1', wav_file])

        return (wav_file, None)  # No phonemes

class ElevenLabsTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(ElevenLabsTTSValidator, self).__init__(tts)

    def validate_lang(self):
        # Assuming Eleven Labs API supports the language set in Mycroft
        return True

    def validate_connection(self):
        # Assuming the API key and voice ID are correct
        return True

    def get_tts_class(self):
        return ElevenLabsTTS
