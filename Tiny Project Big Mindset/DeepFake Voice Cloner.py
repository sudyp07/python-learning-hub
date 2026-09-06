#!/usr/bin/env python3
"""
DeepFake Voice Cloner with Text-to-Speech - Single File Project
Features:
- Clone voices using 5-10 seconds of audio
- Text-to-speech in cloned voice
- Adjust pitch, speed, and emotion
- Mix multiple voices
- Real-time voice preview
- Export to WAV/MP3
"""

import os
import sys
import json
import wave
import struct
import tempfile
import threading
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

# Audio processing
try:
    import soundfile as sf
    import sounddevice as sd
    from scipy import signal
    from scipy.io import wavfile
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("⚠️  Audio libraries not available. Install: pip install soundfile sounddevice scipy")

# Deep Learning
try:
    import torch
    import torchaudio
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️  PyTorch not available. Install: pip install torch torchaudio")

# TTS
try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  TTS not available. Install: pip install TTS")

# GUI
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, scrolledtext, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("⚠️  Tkinter not available. CLI mode only.")

# ============== CONSTANTS ==============

VOICE_MODELS = {
    "xtts_v2": "tts_models/multilingual/multi-dataset/xtts_v2",
    "vits": "tts_models/en/ljspeech/tacotron2-DDC",
    "glow_tts": "tts_models/en/ljspeech/glow-tts",
    "fastspeech": "tts_models/en/ljspeech/fastspeech2",
}

EMOTIONS = {
    "neutral": 0.0,
    "happy": 0.3,
    "sad": -0.2,
    "angry": 0.4,
    "excited": 0.5,
    "calm": -0.3,
}

LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
}

# ============== VOICE CLONER ==============

class VoiceCloner:
    """Main voice cloning engine"""
    
    def __init__(self):
        self.tts = None
        self.model_name = "xtts_v2"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.speaker_embeddings = {}
        self.voice_samples = {}
        self.is_initialized = False
        self.sample_rate = 24000
        
        print(f"🔧 Using device: {self.device}")
        self.initialize_tts()
    
    def initialize_tts(self):
        """Initialize the TTS engine"""
        if not TTS_AVAILABLE or not TORCH_AVAILABLE:
            print("❌ TTS or PyTorch not available")
            return False
        
        try:
            print(f"📦 Loading TTS model: {self.model_name}...")
            self.tts = TTS(model_name=VOICE_MODELS[self.model_name], progress_bar=False)
            self.is_initialized = True
            print("✅ TTS model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize TTS: {e}")
            return False
    
    def list_voices(self) -> List[str]:
        """List available TTS voices"""
        if not self.tts:
            return []
        
        try:
            # For XTTS, we can get speaker list
            if hasattr(self.tts, "speaker_manager") and self.tts.speaker_manager:
                return list(self.tts.speaker_manager.speakers.keys())
            return []
        except:
            return []
    
    def clone_voice(self, audio_path: str, text: str, 
                   language: str = "en",
                   speed: float = 1.0,
                   emotion: str = "neutral",
                   pitch_shift: float = 0.0,
                   output_path: str = None) -> Optional[str]:
        """
        Clone voice and generate speech
        
        Args:
            audio_path: Path to reference audio (5-10 seconds)
            text: Text to synthesize
            language: Language code (en, es, fr, etc.)
            speed: Speech speed (0.5 to 2.0)
            emotion: Emotion to apply
            pitch_shift: Pitch shift in semitones (-12 to 12)
            output_path: Output path (auto-generated if None)
        
        Returns:
            Path to generated audio file
        """
        if not self.is_initialized:
            print("❌ TTS not initialized")
            return None
        
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return None
        
        if not text.strip():
            print("❌ Text is empty")
            return None
        
        try:
            # Generate output path
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"cloned_voice_{timestamp}.wav"
            
            print(f"🎤 Cloning voice from: {os.path.basename(audio_path)}")
            print(f"📝 Text: {text[:50]}...")
            
            # Clone and generate using XTTS
            if self.model_name == "xtts_v2":
                # Generate speech with cloned voice
                self.tts.tts_to_file(
                    text=text,
                    speaker_wav=audio_path,
                    language=language,
                    file_path=output_path,
                    speed=speed
                )
            else:
                # Use standard TTS for other models
                self.tts.tts_to_file(
                    text=text,
                    file_path=output_path
                )
            
            # Apply pitch shift and emotion if needed
            if pitch_shift != 0.0 or emotion != "neutral":
                self._apply_effects(output_path, output_path, 
                                   pitch_shift, speed, emotion)
            
            print(f"✅ Voice cloned successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Voice cloning failed: {e}")
            return None
    
    def clone_with_multiple_voices(self, audio_paths: List[str], 
                                   text: str,
                                   weights: List[float] = None,
                                   **kwargs) -> Optional[str]:
        """
        Clone voice by mixing multiple reference voices
        
        Args:
            audio_paths: List of reference audio files
            text: Text to synthesize
            weights: Weight for each voice (sum to 1.0)
            **kwargs: Additional parameters for clone_voice
        """
        if not audio_paths:
            print("❌ No audio paths provided")
            return None
        
        if weights is None:
            weights = [1.0 / len(audio_paths)] * len(audio_paths)
        else:
            weights = np.array(weights) / sum(weights)
        
        print(f"🎭 Mixing {len(audio_paths)} voices...")
        
        # Generate individual voice clones
        temp_files = []
        for i, (path, weight) in enumerate(zip(audio_paths, weights)):
            temp_path = f"temp_voice_{i}.wav"
            result = self.clone_voice(path, text, output_path=temp_path, **kwargs)
            if result:
                temp_files.append((result, weight))
        
        if not temp_files:
            return None
        
        # Mix the audio files
        output_path = f"mixed_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        self._mix_audio_files(temp_files, output_path)
        
        # Cleanup temp files
        for temp_file, _ in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass
        
        print(f"✅ Mixed voice created: {output_path}")
        return output_path
    
    def _apply_effects(self, input_path: str, output_path: str,
                      pitch_shift: float, speed: float, emotion: str):
        """Apply audio effects like pitch shift and speed"""
        try:
            data, sr = sf.read(input_path)
            
            # Apply speed change
            if speed != 1.0:
                data = signal.resample(data, int(len(data) / speed))
            
            # Apply pitch shift (using FFT)
            if pitch_shift != 0.0:
                # Simple pitch shift using phase vocoder
                n_steps = pitch_shift
                data = self._pitch_shift(data, sr, n_steps)
            
            # Apply emotion (volume/energy modulation)
            if emotion in EMOTIONS:
                emotion_factor = EMOTIONS[emotion]
                # Simple modulation for demonstration
                if abs(emotion_factor) > 0.1:
                    # Adjust dynamics based on emotion
                    data = self._apply_emotion(data, emotion_factor)
            
            # Save processed audio
            sf.write(output_path, data, sr)
            
        except Exception as e:
            print(f"⚠️  Failed to apply effects: {e}")
    
    def _pitch_shift(self, data: np.ndarray, sr: int, n_steps: int) -> np.ndarray:
        """Simple pitch shift using FFT"""
        # This is a simplified pitch shift
        # For production, use a proper phase vocoder
        if n_steps == 0:
            return data
        
        # Stretch factor
        factor = 2 ** (n_steps / 12)
        
        # Use scipy's resample for speed change
        from scipy import signal
        new_len = int(len(data) / factor)
        data_shifted = signal.resample(data, new_len)
        
        # Resample back to original length
        data_final = signal.resample(data_shifted, len(data))
        
        return data_final
    
    def _apply_emotion(self, data: np.ndarray, factor: float) -> np.ndarray:
        """Apply emotional modulation to audio"""
        # Simple dynamic modulation
        # Positive factor = more energetic, negative = calmer
        if factor > 0:
            # Boost attack
            envelope = np.linspace(1.0, 1.0 + factor * 0.3, len(data))
            data = data * envelope
        else:
            # Soften
            envelope = np.linspace(1.0, 1.0 + factor * 0.3, len(data))
            data = data * envelope
        
        return data
    
    def _mix_audio_files(self, files: List[Tuple[str, float]], output_path: str):
        """Mix multiple audio files with weights"""
        if not files:
            return
        
        # Load all files
        audio_data = []
        sr = None
        
        for file_path, weight in files:
            data, sample_rate = sf.read(file_path)
            if sr is None:
                sr = sample_rate
            elif sr != sample_rate:
                # Resample to match
                from scipy import signal
                data = signal.resample(data, int(len(data) * sr / sample_rate))
            
            audio_data.append((data, weight))
        
        # Mix
        max_len = max(len(data) for data, _ in audio_data)
        mixed = np.zeros(max_len)
        
        for data, weight in audio_data:
            # Pad or trim to max_len
            if len(data) < max_len:
                data = np.pad(data, (0, max_len - len(data)))
            else:
                data = data[:max_len]
            mixed += data * weight
        
        # Normalize
        if np.max(np.abs(mixed)) > 0:
            mixed = mixed / np.max(np.abs(mixed))
        
        # Save
        sf.write(output_path, mixed, sr)
    
    def record_voice(self, duration: int = 5, sample_rate: int = 24000) -> Optional[str]:
        """Record voice from microphone"""
        if not AUDIO_AVAILABLE:
            print("❌ Audio libraries not available")
            return None
        
        try:
            import sounddevice as sd
            
            print(f"🎤 Recording for {duration} seconds...")
            print("Speak clearly into the microphone")
            print("3...")
            time.sleep(1)
            print("2...")
            time.sleep(1)
            print("1...")
            time.sleep(1)
            
            # Record
            audio_data = sd.rec(int(duration * sample_rate), 
                               samplerate=sample_rate, 
                               channels=1, 
                               dtype='float32')
            sd.wait()
            
            # Save
            output_path = f"recorded_voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            sf.write(output_path, audio_data, sample_rate)
            
            print(f"✅ Recording saved: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Recording failed: {e}")
            return None
    
    def play_audio(self, file_path: str):
        """Play audio file"""
        if not AUDIO_AVAILABLE:
            print("❌ Audio libraries not available")
            return
        
        try:
            data, sr = sf.read(file_path)
            import sounddevice as sd
            sd.play(data, sr)
            sd.wait()
        except Exception as e:
            print(f"❌ Playback failed: {e}")
    
    def batch_process(self, texts: List[str], audio_path: str, 
                     output_dir: str = "batch_output") -> List[str]:
        """Process multiple texts with the same voice"""
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for i, text in enumerate(texts):
            output_path = os.path.join(output_dir, f"output_{i:04d}.wav")
            result = self.clone_voice(audio_path, text, output_path=output_path)
            if result:
                results.append(result)
        
        return results

# ============== GUI APPLICATION ==============

class VoiceClonerGUI:
    """Tkinter GUI for Voice Cloner"""
    
    def __init__(self):
        if not GUI_AVAILABLE:
            print("❌ Tkinter not available")
            return
        
        self.root = tk.Tk()
        self.root.title("🎭 DeepFake Voice Cloner")
        self.root.geometry("900x750")
        self.root.configure(bg='#2b2b2b')
        
        self.cloner = VoiceCloner()
        self.voice_samples = {}
        self.current_audio = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI interface"""
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Dark.TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('Dark.TButton', background='#4a4a4a', foreground='#ffffff')
        style.map('Dark.TButton', background=[('active', '#5a5a5a')])
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="10")
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="🎭 DeepFake Voice Cloner",
                               font=('Arial', 20, 'bold'),
                               style='Dark.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Voice Input Section
        voice_frame = ttk.LabelFrame(main_frame, text="Voice Input", 
                                     style='Dark.TFrame', padding="10")
        voice_frame.pack(fill='x', pady=(0, 10))
        
        # Buttons for voice input
        btn_frame = ttk.Frame(voice_frame, style='Dark.TFrame')
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="📁 Load Voice File", 
                  command=self.load_voice_file, style='Dark.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="🎤 Record Voice", 
                  command=self.record_voice, style='Dark.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="▶️ Play Sample", 
                  command=self.play_sample, style='Dark.TButton').pack(side='left', padx=5)
        
        self.voice_status = ttk.Label(voice_frame, text="No voice loaded", 
                                      style='Dark.TLabel')
        self.voice_status.pack(pady=(10, 0))
        
        # Voice Preview (waveform visualization placeholder)
        self.voice_preview = ttk.Label(voice_frame, text="", style='Dark.TLabel')
        self.voice_preview.pack(pady=(5, 0))
        
        # TTS Settings Section
        settings_frame = ttk.LabelFrame(main_frame, text="TTS Settings",
                                        style='Dark.TFrame', padding="10")
        settings_frame.pack(fill='x', pady=(0, 10))
        
        # Settings grid
        grid_frame = ttk.Frame(settings_frame, style='Dark.TFrame')
        grid_frame.pack(fill='x')
        
        # Language
        ttk.Label(grid_frame, text="Language:", style='Dark.TLabel').grid(row=0, column=0, sticky='w', padx=5)
        self.lang_var = tk.StringVar(value="en")
        lang_combo = ttk.Combobox(grid_frame, textvariable=self.lang_var, 
                                 values=list(LANGUAGES.keys()), width=10)
        lang_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Speed
        ttk.Label(grid_frame, text="Speed:", style='Dark.TLabel').grid(row=0, column=2, sticky='w', padx=5)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(grid_frame, from_=0.5, to=2.0, 
                               variable=self.speed_var, orient='horizontal', length=100)
        speed_scale.grid(row=0, column=3, padx=5, pady=5)
        self.speed_label = ttk.Label(grid_frame, text="1.0x", style='Dark.TLabel')
        self.speed_label.grid(row=0, column=4, padx=5)
        
        # Pitch
        ttk.Label(grid_frame, text="Pitch:", style='Dark.TLabel').grid(row=1, column=0, sticky='w', padx=5)
        self.pitch_var = tk.DoubleVar(value=0.0)
        pitch_scale = ttk.Scale(grid_frame, from_=-12, to=12, 
                               variable=self.pitch_var, orient='horizontal', length=100)
        pitch_scale.grid(row=1, column=1, padx=5, pady=5)
        self.pitch_label = ttk.Label(grid_frame, text="0.0", style='Dark.TLabel')
        self.pitch_label.grid(row=1, column=2, padx=5)
        
        # Emotion
        ttk.Label(grid_frame, text="Emotion:", style='Dark.TLabel').grid(row=1, column=3, sticky='w', padx=5)
        self.emotion_var = tk.StringVar(value="neutral")
        emotion_combo = ttk.Combobox(grid_frame, textvariable=self.emotion_var,
                                    values=list(EMOTIONS.keys()), width=10)
        emotion_combo.grid(row=1, column=4, padx=5, pady=5)
        
        # Text Input Section
        text_frame = ttk.LabelFrame(main_frame, text="Text to Speak",
                                    style='Dark.TFrame', padding="10")
        text_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.text_input = scrolledtext.ScrolledText(text_frame, height=5,
                                                    bg='#3c3c3c', fg='#ffffff',
                                                    font=('Arial', 11))
        self.text_input.pack(fill='both', expand=True)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        control_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(control_frame, text="🎤 Generate Voice", 
                  command=self.generate_voice, style='Dark.TButton').pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="▶️ Play Generated", 
                  command=self.play_generated, style='Dark.TButton').pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="💾 Export", 
                  command=self.export_audio, style='Dark.TButton').pack(side='left', padx=5)
        
        ttk.Button(control_frame, text="🎭 Mix Voices", 
                  command=self.mix_voices, style='Dark.TButton').pack(side='left', padx=5)
        
        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", 
                                    style='Dark.TLabel', relief='sunken')
        self.status_bar.pack(fill='x', pady=(10, 0))
        
        # Bind scale updates
        speed_scale.bind('<Motion>', self.update_speed_label)
        pitch_scale.bind('<Motion>', self.update_pitch_label)
    
    def update_speed_label(self, event=None):
        self.speed_label.config(text=f"{self.speed_var.get():.1f}x")
    
    def update_pitch_label(self, event=None):
        pitch = self.pitch_var.get()
        self.pitch_label.config(text=f"{pitch:+.1f}")
    
    def load_voice_file(self):
        """Load voice file from disk"""
        file_path = filedialog.askopenfilename(
            title="Select Voice Audio",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac *.m4a"), 
                      ("All files", "*.*")]
        )
        
        if file_path:
            try:
                data, sr = sf.read(file_path)
                duration = len(data) / sr
                
                if duration < 3:
                    messagebox.showwarning("Short Audio", 
                        "Audio is shorter than 3 seconds. For best results, use 5-10 seconds.")
                
                self.voice_samples['main'] = file_path
                self.voice_status.config(text=f"✅ Loaded: {os.path.basename(file_path)} ({duration:.1f}s)")
                self.status_bar.config(text=f"Voice loaded: {os.path.basename(file_path)}")
                
                # Try to play preview
                self.play_audio(file_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load audio: {e}")
    
    def record_voice(self):
        """Record voice from microphone"""
        if not AUDIO_AVAILABLE:
            messagebox.showerror("Error", "Audio libraries not available")
            return
        
        try:
            # Ask for duration
            duration = tk.simpledialog.askinteger("Recording", 
                                                 "Recording duration (seconds):", 
                                                 initialvalue=5, minvalue=3, maxvalue=30)
            if duration is None:
                return
            
            self.status_bar.config(text=f"Recording for {duration} seconds...")
            
            # Record
            file_path = self.cloner.record_voice(duration)
            
            if file_path:
                self.voice_samples['main'] = file_path
                self.voice_status.config(text=f"✅ Recorded: {os.path.basename(file_path)} ({duration}s)")
                self.status_bar.config(text="Recording complete")
                
                # Play back the recording
                self.play_audio(file_path)
            else:
                self.status_bar.config(text="Recording failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Recording failed: {e}")
    
    def play_sample(self):
        """Play the loaded voice sample"""
        if 'main' in self.voice_samples:
            self.play_audio(self.voice_samples['main'])
        else:
            messagebox.showwarning("No Voice", "Please load or record a voice first")
    
    def generate_voice(self):
        """Generate voice from text"""
        if 'main' not in self.voice_samples:
            messagebox.showwarning("No Voice", "Please load or record a voice first")
            return
        
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to speak")
            return
        
        self.status_bar.config(text="Generating voice...")
        
        # Get parameters
        language = self.lang_var.get()
        speed = self.speed_var.get()
        pitch = self.pitch_var.get()
        emotion = self.emotion_var.get()
        
        # Generate
        output_path = self.cloner.clone_voice(
            audio_path=self.voice_samples['main'],
            text=text,
            language=language,
            speed=speed,
            pitch_shift=pitch,
            emotion=emotion
        )
        
        if output_path:
            self.current_audio = output_path
            self.status_bar.config(text=f"Voice generated: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", "Voice generated successfully!")
            self.play_audio(output_path)
        else:
            self.status_bar.config(text="Generation failed")
    
    def play_generated(self):
        """Play the generated audio"""
        if self.current_audio and os.path.exists(self.current_audio):
            self.play_audio(self.current_audio)
        else:
            messagebox.showwarning("No Audio", "Please generate voice first")
    
    def export_audio(self):
        """Export generated audio"""
        if not self.current_audio or not os.path.exists(self.current_audio):
            messagebox.showwarning("No Audio", "Please generate voice first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav"), ("MP3 files", "*.mp3"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.current_audio, file_path)
                self.status_bar.config(text=f"Exported to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Audio exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")
    
    def mix_voices(self):
        """Mix multiple voices"""
        # Get multiple voice files
        file_paths = filedialog.askopenfilenames(
            title="Select Voice Files to Mix",
            filetypes=[("Audio files", "*.wav *.mp3 *.flac"), ("All files", "*.*")]
        )
        
        if not file_paths:
            return
        
        if len(file_paths) < 2:
            messagebox.showwarning("Not Enough Voices", "Select at least 2 voices to mix")
            return
        
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to speak")
            return
        
        self.status_bar.config(text="Mixing voices...")
        
        # Mix voices
        output_path = self.cloner.clone_with_multiple_voices(
            audio_paths=list(file_paths),
            text=text,
            language=self.lang_var.get(),
            speed=self.speed_var.get(),
            emotion=self.emotion_var.get()
        )
        
        if output_path:
            self.current_audio = output_path
            self.status_bar.config(text=f"Mixed voice generated: {os.path.basename(output_path)}")
            messagebox.showinfo("Success", "Mixed voice generated successfully!")
            self.play_audio(output_path)
        else:
            self.status_bar.config(text="Voice mixing failed")
    
    def play_audio(self, file_path: str):
        """Play audio file"""
        if not AUDIO_AVAILABLE:
            return
        
        try:
            data, sr = sf.read(file_path)
            import sounddevice as sd
            sd.play(data, sr)
            sd.wait()
        except Exception as e:
            print(f"Playback failed: {e}")
    
    def run(self):
        """Run the GUI application"""
        self.root.mainloop()

# ============== CLI INTERFACE ==============

class VoiceClonerCLI:
    """Command line interface"""
    
    def __init__(self):
        self.cloner = VoiceCloner()
        self.current_voice = None
    
    def run(self):
        """Run CLI"""
        self.show_welcome()
        
        while True:
            try:
                command = input("\n🎭 > ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'load':
                    self.load_voice(parts[1] if len(parts) > 1 else None)
                elif cmd == 'record':
                    self.record_voice()
                elif cmd == 'generate':
                    self.generate_voice(' '.join(parts[1:]) if len(parts) > 1 else None)
                elif cmd == 'play':
                    self.play_voice()
                elif cmd == 'mix':
                    self.mix_voices()
                elif cmd == 'batch':
                    self.batch_process()
                elif cmd == 'list':
                    self.list_voices()
                elif cmd == 'info':
                    self.show_info()
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_welcome(self):
        """Show welcome message"""
        print("\n" + "="*60)
        print("🎭 DEEPFAKE VOICE CLONER with Text-to-Speech")
        print("="*60)
        print("\n🔊 Clone voices using just 5 seconds of audio!")
        print("📝 Convert text to speech in cloned voice")
        print("🎨 Adjust pitch, speed, and emotion")
        print("\nType 'help' for commands")
        print("="*60)
    
    def show_help(self):
        """Show help"""
        print("\n" + "="*60)
        print("🎭 Available Commands:")
        print("="*60)
        print("\n  📁 load <file>     - Load voice audio file")
        print("  🎤 record          - Record voice from microphone")
        print("  📝 generate <text> - Generate speech in cloned voice")
        print("  ▶️ play            - Play generated audio")
        print("  🎭 mix             - Mix multiple voices")
        print("  📋 list            - List available TTS voices")
        print("  📊 batch           - Batch process multiple texts")
        print("  ℹ️ info            - Show system info")
        print("  ❓ help            - Show this help")
        print("  🚪 quit            - Exit")
        print("\n" + "="*60)
    
    def load_voice(self, file_path: str):
        """Load voice file"""
        if not file_path:
            print("❌ Please provide a file path: load <file>")
            return
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        try:
            data, sr = sf.read(file_path)
            duration = len(data) / sr
            self.current_voice = file_path
            print(f"✅ Loaded voice: {os.path.basename(file_path)} ({duration:.1f}s)")
        except Exception as e:
            print(f"❌ Failed to load audio: {e}")
    
    def record_voice(self):
        """Record voice"""
        file_path = self.cloner.record_voice()
        if file_path:
            self.current_voice = file_path
            print(f"✅ Voice recorded: {os.path.basename(file_path)}")
    
    def generate_voice(self, text: str):
        """Generate voice"""
        if not self.current_voice:
            print("❌ No voice loaded. Use 'load' or 'record' first")
            return
        
        if not text:
            text = input("Enter text to speak: ").strip()
            if not text:
                print("❌ Text cannot be empty")
                return
        
        # Show options
        speed = input("Speed (0.5-2.0, default 1.0): ").strip()
        speed = float(speed) if speed else 1.0
        
        pitch = input("Pitch shift (-12 to 12, default 0): ").strip()
        pitch = float(pitch) if pitch else 0.0
        
        emotion = input(f"Emotion ({'/'.join(EMOTIONS.keys())}, default neutral): ").strip()
        if emotion not in EMOTIONS:
            emotion = "neutral"
        
        # Generate
        print("🎤 Generating voice...")
        output = self.cloner.clone_voice(
            self.current_voice,
            text,
            speed=speed,
            pitch_shift=pitch,
            emotion=emotion
        )
        
        if output:
            print(f"✅ Generated: {output}")
            play = input("Play audio? (y/n): ").strip().lower()
            if play == 'y':
                self.cloner.play_audio(output)
    
    def play_voice(self):
        """Play generated audio"""
        if self.cloner.current_audio:
            self.cloner.play_audio(self.cloner.current_audio)
        else:
            print("❌ No generated audio to play")
    
    def mix_voices(self):
        """Mix multiple voices"""
        files = input("Enter paths to audio files (space-separated): ").strip().split()
        if len(files) < 2:
            print("❌ Need at least 2 audio files")
            return
        
        text = input("Enter text to speak: ").strip()
        if not text:
            print("❌ Text cannot be empty")
            return
        
        print("🎭 Mixing voices...")
        output = self.cloner.clone_with_multiple_voices(files, text)
        
        if output:
            print(f"✅ Mixed voice generated: {output}")
    
    def batch_process(self):
        """Batch process multiple texts"""
        if not self.current_voice:
            print("❌ No voice loaded")
            return
        
        input_file = input("Enter input file with texts (one per line): ").strip()
        if not os.path.exists(input_file):
            print("❌ Input file not found")
            return
        
        with open(input_file, 'r') as f:
            texts = [line.strip() for line in f if line.strip()]
        
        print(f"📊 Processing {len(texts)} texts...")
        results = self.cloner.batch_process(texts, self.current_voice)
        print(f"✅ Generated {len(results)} audio files")
    
    def list_voices(self):
        """List available TTS voices"""
        voices = self.cloner.list_voices()
        if voices:
            print(f"\n📋 Available Voices ({len(voices)}):")
            for voice in voices[:10]:
                print(f"  • {voice}")
            if len(voices) > 10:
                print(f"  ... and {len(voices)-10} more")
        else:
            print("ℹ️  No additional voices available")
    
    def show_info(self):
        """Show system info"""
        print("\nℹ️ System Information")
        print("-"*40)
        print(f"  PyTorch Available: {TORCH_AVAILABLE}")
        print(f"  TTS Available: {TTS_AVAILABLE}")
        print(f"  CUDA Available: {torch.cuda.is_available() if TORCH_AVAILABLE else False}")
        print(f"  Device: {self.cloner.device}")
        print(f"  Audio Libraries: {'✅' if AUDIO_AVAILABLE else '❌'}")
        print(f"  GUI Available: {'✅' if GUI_AVAILABLE else '❌'}")

# ============== MAIN ==============

def main():
    """Main entry point"""
    print("\n🚀" + "="*58)
    print("  DEEPFAKE VOICE CLONER WITH TEXT-TO-SPEECH")
    print("="*58 + "🚀")
    
    # Check dependencies
    if not TTS_AVAILABLE:
        print("\n❌ TTS not installed. Install with:")
        print("   pip install TTS")
        return
    
    if not TORCH_AVAILABLE:
        print("\n❌ PyTorch not installed. Install with:")
        print("   pip install torch torchaudio")
        return
    
    # Check for GUI mode
    if len(sys.argv) > 1:
        if sys.argv[1] == '--gui' and GUI_AVAILABLE:
            gui = VoiceClonerGUI()
            gui.run()
            return
        elif sys.argv[1] == '--help':
            print("""
Usage:
  python voice_cloner.py              - CLI mode
  python voice_cloner.py --gui        - GUI mode
  python voice_cloner.py --help       - Show this help
            """)
            return
    
    # CLI mode (default)
    cli = VoiceClonerCLI()
    cli.run()

if __name__ == "__main__":
    main()