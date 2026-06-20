# Coding Standards 

## Code Style & Formatting (The "No Debate" Rule)
* **Formatter: Black**: Before committing to GitHub, must run `black .` in terminal. If Black formats it, that is the standard. 
* **Linter: Flake8:** Run `flake8` to catch undefined variables or unused imports before pushing.
* **Max Line Length:** 88 characters (Black's default)

--- 

## Naming Conventions
* **Variables & Functions:** `snake_case` (e.g. `extract_audio()` or `video_file_path`)
* **Constants & Parameters:** `UPPER_SNAKE_CASE` (e.g. `MAX_FILE_SIZE_MB = 50`, `GROQ_MODEL = "whisper-large-v3-turbo"`)
* **Classes:** `PascalCase` (e.g. class InterviewAnalyzer)

--- 

## Documentation & Comments 
* **Docstrings:** Use the **Google Docstring Format** for all major functions. It is highly readable and works great with IDEs and AI agents.
```python
def extract_audio(video_path: str) -> str:
    """
    Strips the audio track from an uploaded video file.

    Args:
        video_path (str): The local path to the temporary video file.

    Returns:
        str: The local path to the generated .mp3 audio file.
    """
```

* Inline Comments: comment why you are doing something, not what you are doing. The code ought to explain the 'what'.

--- 

## Security 
* **NEVER** hardcode API keys 
* Use the `python-dotenv` package.
* Store any key in a local .env file. 
* Ensure .env is in .gitignore

--- 

## Install 
```python
pip install black flake8 python-dotenv
```
