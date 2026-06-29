import os
import time

import whisper

from utils.logger import Logger


class LocalTranscriber:
    """Handles on-device speech-to-text using local Whisper models."""

    def __init__(self, MODEL_SIZE: str = "medium") -> None:
        """
        Initializes the transcriber and loads the model into local memory.
        Warning: Loading the model takes a few seconds.

        Args:
            MODEL_SIZE (str): the size of the whisper model, available choices : tiny
                base
                small
                medium
                large
                large-v2
                large-v3,
        """
        Logger.log_info(f"Loading local Whisper model ('{MODEL_SIZE}')...")
        start_load = time.time()

        # - - - This downloads the model weights the first time you run it
        self.model = whisper.load_model(MODEL_SIZE)

        load_time = time.time() - start_load
        Logger.log_debug(f"Model loaded into memory in {load_time:.2f} seconds.")

    def transcribe_binary(
        self,
        AUDIO_BYTES: bytes,
        FILE_EXTENSION: str = "mp3",
        LANGUAGE: str = "en",
    ) -> dict[str, any]:
        """
        Takes raw audio bytes, temporarily writes them to disk,
        transcribes them locally, and enforces zero-retention cleanup.

        Args:
            AUDIO_BYTES (bytes): The audio buffer
            FILE_EXTENSION (str): Optional file extension to detect codec
            LANGUAGE (str): Optional language to force the transcription in

        Returns:
            dict[str, Any]: The transcription result which is the full whisper dictionary containing text, segments, and word-level timestamps.
        """
        temp_filename = f"temp_transcription_buffer.{FILE_EXTENSION}"

        try:
            # - - - 1. Write binary array to a temporary local file
            with open(temp_filename, "wb") as temp_file:
                temp_file.write(AUDIO_BYTES)
            Logger.log_debug(f"Temporary audio buffer written to {temp_filename}.")

            # - - - 2. Run the local transcription and benchmark it
            Logger.log_info("Starting local transcription engine...")
            start_transcribe = time.time()

            # - - - fp16=False prevents warnings on CPUs/standard laptops
            if LANGUAGE:
                result = self.model.transcribe(
                    temp_filename, fp16=False, language=LANGUAGE, word_timestamps=True
                )
            else:
                result = self.model.transcribe(temp_filename, fp16=False)
            Logger.log_debug(f"Language:  {result['language']}")

            process_time = time.time() - start_transcribe

            # - - - 3. Log the performance metrics
            Logger.log_info(f"Transcription complete in {process_time:.2f} seconds.")

            return result

        except Exception as e:
            Logger.log_error(f"Local transcription failed: {str(e)}")
            raise

        finally:
            # - - - 4. Zero-Retention: Guarantee the file is deleted even if it crashes
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                Logger.log_debug("Temporary audio buffer securely deleted.")
