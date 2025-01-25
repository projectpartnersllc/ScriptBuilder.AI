from deepgram import DeepgramClient

# Initialize the Deepgram client
DG_KEY = "api key"  # Replace with your API key
deepgram = DeepgramClient(DG_KEY)


def transcribe_audio_file(audio_file_path):
    """
    Transcribes the audio file using Deepgram API.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        dict: Response from Deepgram API.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            buffer_data = audio_file.read()

        options = {
            "model": "nova-2",
            "smart_format": True,
            "language": "en",
            "diarize": True,
            "profanity_filter": False,
        }
        
        payload = {
            "buffer": buffer_data,
        }

        # Use the new rest method instead of prerecorded
        response = deepgram.listen.rest.transcribe(buffer_data, **options)
        return response
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def process_diarized_transcript(res):
    """
    Processes the diarized transcript into speaker-segmented text.

    Args:
        res (dict): Response from Deepgram API.

    Returns:
        list: List of tuples with speaker and corresponding sentences.
    """
    if not res or 'results' not in res or 'channels' not in res['results']:
        return []

    transcript = res['results']['channels'][0]['alternatives'][0]
    words = transcript['words']

    current_speaker = None
    current_sentence = []
    output = []

    for word in words:
        if current_speaker != word['speaker']:
            if current_sentence:
                output.append((current_speaker, ' '.join(current_sentence)))
                current_sentence = []
            current_speaker = word['speaker']

        current_sentence.append(word['punctuated_word'])

        if word['punctuated_word'].endswith(('.', '?', '!')):
            output.append((current_speaker, ' '.join(current_sentence)))
            current_sentence = []

    if current_sentence:
        output.append((current_speaker, ' '.join(current_sentence)))

    return output


def format_speaker(speaker_num):
    """
    Formats the speaker identifier.

    Args:
        speaker_num (int): Speaker number.

    Returns:
        str: Formatted speaker identifier.
    """
    return f"Speaker {speaker_num}"


def transcribe_and_process_audio(audio_file_path):
    """
    Transcribes and processes the audio file.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Formatted transcription string.
    """
    res = transcribe_audio_file(audio_file_path)
    if not res:
        return "No transcription available."

    diarized_result = process_diarized_transcript(res)

    if not diarized_result:
        return "No transcription available. The audio might be of low quality or silent."

    transcription = ""

    for speaker, sentence in diarized_result:
        transcription += f"{format_speaker(speaker)}: {sentence}\n"

    return transcription


def main():
    """
    Main function to transcribe and print the audio file transcription.
    """
    audio_file_path = r"c:\Users\Dell\Downloads\Weekly_Meeting_Example(256k).mp3"  # Update with your file path

    print("Transcribing audio file...")
    transcript = transcribe_and_process_audio(audio_file_path)
    print("\nTranscription:\n")
    print(transcript)


if __name__ == "__main__":
    main()
