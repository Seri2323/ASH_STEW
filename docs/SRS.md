# SRS : Projerkt MVP  

## Introduction 

### Purpose
The software is a web app focused on helping college students practice interviews and get automated feedback on speech clarity, filler word usage, and answer structure without storing user data or requiring human intervention.

### Scope
MVP will be focused on behavioral and HR interview scenarios.
* **In scope**:
  * Secure video / audio upload 
  * Automatic speech-to-text transcription
  * Filler word analysis 
  * LLM driven qualitative feedback 
* **Out of Scope**
  * Coding assessments 
  * Real time interviewing
  * Facial emotion analysis 
  * Edge AI 

--- 

## Description

### What does it do?
User uploads a pre-recorded video of themselves answering common interview questions. The application splits the file into audio and video components, transcribes the speech, and evaluates the performance. Within seconds, the user receives a Report Card detailing their metrics and feedback on their answer and a gaurantee that the uploaded data is destroyed instantly after analysis (The fact that I dont want to pay for the storage is irrelevant).

### User Classes & Characteristics
Made with a single primary user in mind. _The Anxious / Shy Job Seeker_: The user may have technical competence (optional) but limited confidence in behavioral / verbal communication. Suffers from stage fright or judgement anxiety during mock interviews with peers or mentors etc.
* **Needs**: Non-judgemental feedback loop. Immediate reinforcement of what they did right, and highly specific, constructive guidance on what to fix.
* **Assumes**: Capable of recording a video and uploading files and reading text.

### Design Constraints 
* **Local Hardware Limitations**: The development team does not possess high-end local GPUs (my laptop shuts down if the lid is at the wrong angle). Therefore, the system architecture must rely on remote, open-weighted modal endpoints rather than Edge AI.
* **Privacy and Zero Retention:** No video or audio files may be writtent o persistent storage or used for training any model. File handling must occur in temporary, ephemeral memory buffers.
* **Cost Constraints**: The devs have no fixed income source, but many expenses, this project wont be another. 

--- 

## Specific Requirements 

### External Interface Requirements

#### User Interface 
* The system shall present a single page web interface 
* File upload widget restricting inputs to .mp4, .webm, .mkv formats with a max file size limit of 50 MB.
* Analyze button 
* Processing indicator 
* Report card with 
  * Transcription text box 
  * Highlighted metric for filler word count 
  * A markdown formatted feedback from the LLM

#### Software Interface 
[TODO: Stuti]

### Functional Requirements 

#### Feature 1: Local Audio Extraction
* **Description:** To save bandwidth and speed up API calls, the system must extract only the audio track from the uploaded video before sending data to the cloud. 
* **Actor**: User has successfully uploaded a valid video file under max file size 
* **Preconditions**: The system exports a temporary .mp3 file (in memory)
* **Edge Cases**: If the uploaded video has no audio, must catch error
* **Post Conditions**: A temporary in-memory .mp3 file exists, ready for transmission

#### Feature 2: Automated Transcription 
* **Description:** Convert extracted mp3 into timestamped text 
* **Actor**: The temporary mp3 file exists 
* **Post Conditions**: The system stores the resulting string variable in memory

#### Feature 3: Analytics & LLM Grading
* **Description:** The system analyzes the transcript for communication metrics and structural feedback.
* **Preconditions:** The transcript string exists in memory.
* **Action 1 (Local):** A Python script scans the transcript against a hardcoded list of filler words (e.g., "um", "uh", "like", "you know") and generates a count.
* **Action 2 (Cloud):** The system sends the transcript to the llama-3.1-8b-instant model along with the HR Persona System Prompt.
* **Post Conditions:** The Streamlit UI renders the filler word count and the Llama 3 feedback report

### Non Functional Requirements:


#### Performance

#### Safety and Security 

#### Reliability and Availability 

#### Maintainability 

--- 

## User Stories 

