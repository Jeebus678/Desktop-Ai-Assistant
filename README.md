This is a pretty ambitious project with a lot of elements involved, but so far, I have integrated the eleven labs API so that the voice assistant can answer you in any voice that you set. This is a direct branch of the current Mycroft-core (as of writing this) with slight edits to the TTS to include the API. Also, you have to include this under your `mycroft-config edit user`:

{
  "max_allowed_core_version": 21.2,
  "tts": {
    "elevenlabs": {
      "lang": "en-us",
      "voice_id": "voice id here",
      "api_key": "api key here"
    },
    "module": "elevenlabs"
  }
}
