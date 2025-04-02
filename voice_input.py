from vosk import Model, KaldiRecognizer
import sounddevice as sd
import queue
import json

model = Model(lang="en-us")  # You must download the model in advance and place it in the expected folder
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def record_description(duration=5) -> str:
    recognizer = KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        print(f"Recording for {duration} seconds...")
        result_text = ""
        for _ in range(int(duration * 16000 / 8000)):
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                result_text += result.get("text", "") + " "
        # Final flush
        final_result = json.loads(recognizer.FinalResult())
        result_text += final_result.get("text", "")
        print("You said:", result_text.strip())
        return result_text.strip()

# For testing
if __name__ == "__main__":
    print("Description:", record_description())