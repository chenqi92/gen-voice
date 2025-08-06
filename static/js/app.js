// Kitten TTS Web Application
class KittenTTSApp {
    constructor() {
        this.selectedVoice = null;
        this.voices = [];
        this.isGenerating = false;
        this.currentAudio = null;
        
        this.init();
    }

    init() {
        this.setupElements();
        this.setupEventListeners();
        this.loadVoices();
    }

    setupElements() {
        this.textInput = document.getElementById('text-input');
        this.charCount = document.getElementById('char-count');
        this.voiceGrid = document.getElementById('voice-grid');
        this.generateBtn = document.getElementById('generate-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.progressContainer = document.getElementById('progress-container');
        this.progressFill = document.getElementById('progress-fill');
        this.progressText = document.getElementById('progress-text');
        this.audioContainer = document.getElementById('audio-container');
        this.audioPlayer = document.getElementById('audio-player');
    }

    setupEventListeners() {
        // Text input character counter
        this.textInput.addEventListener('input', () => {
            const length = this.textInput.value.length;
            this.charCount.textContent = length;
            this.updateGenerateButton();
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => {
            this.generateSpeech();
        });

        // Download button
        this.downloadBtn.addEventListener('click', () => {
            this.downloadAudio();
        });

        // Enter key in text input
        this.textInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.generateSpeech();
            }
        });
    }

    async loadVoices() {
        try {
            const response = await fetch('/api/voices');
            const data = await response.json();
            
            if (data.voices && data.voices.length > 0) {
                this.voices = data.voices;
                this.renderVoices();
                // Select first voice by default
                this.selectVoice(this.voices[0].id);
            } else {
                this.showError('No voices available');
            }
        } catch (error) {
            console.error('Failed to load voices:', error);
            this.showError('Failed to load voices');
        }
    }

    renderVoices() {
        this.voiceGrid.innerHTML = '';
        
        this.voices.forEach(voice => {
            const voiceCard = document.createElement('div');
            voiceCard.className = 'voice-card';
            voiceCard.dataset.voiceId = voice.id;
            
            const genderClass = voice.gender.toLowerCase();
            const genderText = window.i18n ? window.i18n.t(`voice-${genderClass}`) : voice.gender;
            
            voiceCard.innerHTML = `
                <div class="voice-header">
                    <div class="voice-name">${voice.name}</div>
                    <div class="voice-gender ${genderClass}">${genderText}</div>
                </div>
                <div class="voice-description">${voice.description}</div>
            `;
            
            voiceCard.addEventListener('click', () => {
                this.selectVoice(voice.id);
            });
            
            this.voiceGrid.appendChild(voiceCard);
        });
    }

    selectVoice(voiceId) {
        // Remove previous selection
        document.querySelectorAll('.voice-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Add selection to clicked card
        const selectedCard = document.querySelector(`[data-voice-id="${voiceId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
            this.selectedVoice = voiceId;
            this.updateGenerateButton();
        }
    }

    updateGenerateButton() {
        const hasText = this.textInput.value.trim().length > 0;
        const hasVoice = this.selectedVoice !== null;
        const canGenerate = hasText && hasVoice && !this.isGenerating;
        
        this.generateBtn.disabled = !canGenerate;
    }

    async generateSpeech() {
        const text = this.textInput.value.trim();
        
        if (!text) {
            this.showError(window.i18n ? window.i18n.t('error-empty-text') : 'Please enter some text');
            return;
        }
        
        if (!this.selectedVoice) {
            this.showError(window.i18n ? window.i18n.t('error-no-voice') : 'Please select a voice');
            return;
        }

        this.isGenerating = true;
        this.updateGenerateButton();
        this.showProgress();

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    voice: this.selectedVoice
                })
            });

            const data = await response.json();

            if (data.success) {
                this.displayAudio(data.audio);
                this.showSuccess(window.i18n ? window.i18n.t('success-generated') : 'Speech generated successfully!');
            } else {
                throw new Error(data.error || 'Generation failed');
            }
        } catch (error) {
            console.error('Generation error:', error);
            this.showError(window.i18n ? window.i18n.t('error-generation') : 'Failed to generate speech');
        } finally {
            this.isGenerating = false;
            this.hideProgress();
            this.updateGenerateButton();
        }
    }

    displayAudio(audioBase64) {
        const audioBlob = this.base64ToBlob(audioBase64, 'audio/wav');
        const audioUrl = URL.createObjectURL(audioBlob);
        
        this.audioPlayer.src = audioUrl;
        this.audioContainer.style.display = 'block';
        this.downloadBtn.disabled = false;
        
        // Store current audio data for download
        this.currentAudio = {
            blob: audioBlob,
            url: audioUrl
        };
    }

    async downloadAudio() {
        if (!this.currentAudio) {
            this.showError(window.i18n ? window.i18n.t('error-download') : 'No audio to download');
            return;
        }

        try {
            const text = this.textInput.value.trim();
            
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    voice: this.selectedVoice
                })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `kitten_tts_${this.selectedVoice}.wav`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } else {
                throw new Error('Download failed');
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showError(window.i18n ? window.i18n.t('error-download') : 'Failed to download audio');
        }
    }

    showProgress() {
        this.progressContainer.style.display = 'block';
        this.progressText.textContent = window.i18n ? window.i18n.t('generating') : 'Generating speech...';
        
        // Animate progress bar
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            this.progressFill.style.width = `${progress}%`;
        }, 200);
        
        this.progressInterval = interval;
    }

    hideProgress() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        
        this.progressFill.style.width = '100%';
        setTimeout(() => {
            this.progressContainer.style.display = 'none';
            this.progressFill.style.width = '0%';
        }, 500);
    }

    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        
        const container = document.getElementById('toast-container');
        container.appendChild(toast);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.kittenApp = new KittenTTSApp();
});
