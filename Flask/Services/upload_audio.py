from flask import request, jsonify
import os
from multiprocessing import Process
from Utils.generate_filename import generate_timestamp_based_filename
from Utils.convert_to_wav import convert_to_wav
from Services.Transcribe_audio import transcribe_audio
from config import UPLOAD_FOLDER
# from multiprocessing import Pool
# from threading import Thread


def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Generate a unique filename using timestamp and random suffix
    unique_filename = generate_timestamp_based_filename(file.filename)

    # Save the audio file
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(file_path)

    # Convert to WAV format (if needed)
    wav_file_path = convert_to_wav(file_path)
    metadata = {
        "file_name": file.filename,
        "unique_filename": unique_filename
    }

    # transcription_thread = Thread(
    #     target=transcribe_audio, args=(wav_file_path,))
    # transcription_thread.start()

    # Start the transcription in a background process (using multiprocessing)
    transcription_process = Process(
        target=transcribe_audio, args=(wav_file_path,))
    transcription_process.start()

    # Provide the URL to access the uploaded audio file
    file_url = f"/uploads/{os.path.basename(wav_file_path)}"

    return jsonify({
        "message": "Audio received and transcription started in the background.",
        "file_url": file_url
    }), 200
