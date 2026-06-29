import json

import streamlit

from transcriber.transcriber import LocalTranscriber

# - - - 1. Page configuration
streamlit.set_page_config(page_title="ASH_STEW", page_icon=":)", layout="wide")

# - - - 2. Session state initialization
if "has_result" not in streamlit.session_state:
    streamlit.session_state.has_result = False
if "whisper_data" not in streamlit.session_state:
    streamlit.session_state.whisper_data = None
if "file_bytes" not in streamlit.session_state:
    streamlit.session_state.file_bytes = None
if "file_name" not in streamlit.session_state:
    streamlit.session_state.file_name = None


# - - - Cache the transcriber so dont need to reload the AI model on every page refresh
@streamlit.cache_resource
def load_transcriber() -> LocalTranscriber:
    """
    Initialize and return a LocalTranscriber instance.

    Returns:
        LocalTranscriber: An instance of the LocalTranscriber class.
    """
    return LocalTranscriber(MODEL_SIZE="medium")


def format_time(SECONDS: float) -> str:
    """
    Format a time duration in seconds to a human-readable string.

    Args:
        SECONDS (float): The time duration in seconds.

    Returns:
        str: The formatted time string.
        eg: 85.5 to 01:25
    """
    mins: int = int(SECONDS // 60)
    secs: int = int(SECONDS % 60)
    return f"{mins:02d}:{secs:02d}"


# - - - | The UI | - - -


streamlit.title("ASH_STEW")
streamlit.caption("Stuti needs to work")


# - - - File uploader : Only show the uploader if we have not processed a file yet - - -

if not streamlit.session_state.has_result:
    uploaded_file = streamlit.file_uploader(
        label="Upload a file to transcribe", type=["mp3", "mp4", "webm", "wav"]
    )

    if uploaded_file is not None:
        if streamlit.button("Analyze", type="primary"):
            with streamlit.spinner(
                "Extracting audio and analyzing speech... (This may take many minutes)"
            ):
                # - - - Save the raw bytes to state for the audio player
                streamlit.session_state.file_bytes = uploaded_file.read()
                streamlit.session_state.file_name = uploaded_file.name

                # - - - Run the transcription pipeline
                transcriber: LocalTranscriber = load_transcriber()
                file_extension: str = uploaded_file.name.split(".")[-1]

                try:
                    result = transcriber.transcribe_binary(
                        AUDIO_BYTES=streamlit.session_state.file_bytes,
                        FILE_EXTENSION=file_extension,
                        LANGUAGE="en",
                    )
                    streamlit.session_state.whisper_data = result
                    streamlit.session_state.has_result = True
                    streamlit.rerun()  # - - - UI update

                except Exception as e:
                    streamlit.error(f"An error occurred: {str(e)}")

# - - - Bottom Section: 3 column dashboard
if streamlit.session_state.has_result:
    # - - - Allow the user to reset and try another file
    if streamlit.button("Reset / Upload New File"):
        streamlit.session_state.has_result = False
        streamlit.session_state.whisper_data = None
        streamlit.session_state.file_bytes = None
        streamlit.rerun()

    streamlit.divider()

    # - - - Define the wide layout - - -

    left_col, center_col, right_col = streamlit.columns([1, 2, 1], gap="large")

    # - - - Left Column: Metrics Placeholder
    with left_col:
        streamlit.subheader("Metrics")
        streamlit.info("The Analytics Module is TODO")

    # - - - Center Column: Player and 3 Lines (Written by Gemini)
    with center_col:
        streamlit.subheader("Playback")
        streamlit.audio(streamlit.session_state.file_bytes, format="audio/mp3")
        streamlit.subheader("Transcript")
        segments: dict[str, any] | None = streamlit.session_state.whisper_data
        if segments is not None:
            segments_json = json.dumps(segments.get("segments", []))

            # - - - Inject custom HTML/JS to read the streamlit audio player time
            karaoke_html = f"""
                    <div style="background-color: #1e1e1e; padding: 30px; border-radius: 12px; text-align: center; font-family: sans-serif; box-shadow: inset 0px 0px 10px rgba(0,0,0,0.5);">
                        <div id="prev-line" style="color: #666; font-size: 1.2em; min-height: 1.5em; margin-bottom: 15px; transition: 0.3s; font-style: italic;"></div>
                        <div id="curr-line" style="color: #4da6ff; font-size: 1.8em; font-weight: bold; min-height: 1.5em; margin-bottom: 15px; transition: 0.2s;">Ready to play...</div>
                        <div id="next-line" style="color: #666; font-size: 1.2em; min-height: 1.5em; transition: 0.3s;"></div>
                    </div>

                    <script>
                        const segments = {segments_json};
                        let audioEl = null;

                        // Search for the Streamlit native audio player in the parent window
                        function findAudioPlayer() {{
                            try {{
                                const audios = window.parent.document.getElementsByTagName('audio');
                                if (audios.length > 0) {{
                                    audioEl = audios[0];
                                }}
                            }} catch (e) {{ console.error("Could not link to parent audio:", e); }}
                        }}

                        setInterval(() => {{
                            if (!audioEl) {{ findAudioPlayer(); return; }}

                            const t = audioEl.currentTime;
                            let activeIdx = -1;

                            // Find the segment that matches current time
                            for(let i=0; i<segments.length; i++) {{
                                if (t >= segments[i].start && t <= (segments[i].end + 0.5)) {{
                                    activeIdx = i;
                                    break;
                                }}
                            }}

                            // If silent gap, hold the last spoken segment
                            if (activeIdx === -1) {{
                                for(let i=segments.length-1; i>=0; i--) {{
                                    if (t > segments[i].end) {{
                                        activeIdx = i;
                                        break;
                                    }}
                                }}
                            }}

                            const prevEl = document.getElementById('prev-line');
                            const currEl = document.getElementById('curr-line');
                            const nextEl = document.getElementById('next-line');

                            if (activeIdx >= 0 && activeIdx < segments.length) {{
                                currEl.innerText = segments[activeIdx].text;
                                prevEl.innerText = (activeIdx > 0) ? segments[activeIdx-1].text : "";
                                nextEl.innerText = (activeIdx < segments.length - 1) ? segments[activeIdx+1].text : "";
                            }} else if (segments.length > 0) {{
                                // Fallback before audio starts
                                currEl.innerText = "Press Play...";
                                nextEl.innerText = segments[0].text;
                            }}
                        }}, 150); // check 6 times a second
                    </script>
                    """
            streamlit.iframe(karaoke_html, height=250)

    # - - - Right column: chronological log
    with right_col:
        streamlit.subheader("Transcript Log")

        # - - - Use streamlit's height parameter to create a scrollable container
        with streamlit.container(height=450):
            segment_data = streamlit.session_state.whisper_data
            if segment_data:
                for segment in segment_data.get("segments", []):
                    start_str: str = format_time(segment["start"])
                    streamlit.markdown(f"**`[{start_str}]`** {segment['text']}")
                    streamlit.divider()  # Adds a faint line between segments
