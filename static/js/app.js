/**
 * Enhanced TTS Application
 * Modern, clean implementation with proper error handling
 */

class EnhancedTTSApp {
    constructor() {
        // State management
        this.state = {
            selectedEngine: null,
            selectedVoice: null,
            engines: [],
            voices: [],
            history: [],
            isGenerating: false,
            sidebarOpen: false
        };
        
        // DOM elements
        this.elements = {};
        
        // Initialize app
        this.init();
    }

    async init() {
        try {
            this.setupElements();
            this.setupEventListeners();
            await this.loadEngines();
            await this.loadVoices();
            await this.loadHistory();
            this.updateUI();
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Failed to initialize application');
        }
    }

    setupElements() {
        // Cache DOM elements
        const elementIds = [
            'engine-selector', 'voice-grid', 'text-input', 'char-count',
            'generate-btn', 'download-btn', 'clear-btn', 'import-btn', 'file-input',
            'progress-container', 'progress-fill', 'progress-text',
            'audio-container', 'audio-player', 'sidebar', 'toggle-sidebar-btn',
            'close-sidebar-btn', 'refresh-history-btn', 'clear-history-btn',
            'history-list', 'total-files', 'total-size', 'lang-toggle', 'current-lang'
        ];

        elementIds.forEach(id => {
            this.elements[id] = document.getElementById(id);
        });

        // Validate critical elements
        const criticalElements = ['engine-selector', 'voice-grid', 'text-input', 'generate-btn'];
        const missingElements = criticalElements.filter(id => !this.elements[id]);
        
        if (missingElements.length > 0) {
            throw new Error(`Missing critical elements: ${missingElements.join(', ')}`);
        }
    }

    setupEventListeners() {
        // Text input events
        if (this.elements['text-input']) {
            this.elements['text-input'].addEventListener('input', () => this.handleTextInput());
            this.elements['text-input'].addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                    e.preventDefault();
                    this.generateSpeech();
                }
            });
        }

        // Button events
        const buttonEvents = {
            'generate-btn': () => this.generateSpeech(),
            'download-btn': () => this.downloadAudio(),
            'clear-btn': () => this.clearText(),
            'import-btn': () => this.elements['file-input']?.click(),
            'toggle-sidebar-btn': () => this.toggleSidebar(),
            'close-sidebar-btn': () => this.closeSidebar(),
            'refresh-history-btn': () => this.loadHistory(),
            'clear-history-btn': () => this.clearHistory(),
            'lang-toggle': () => this.toggleLanguage()
        };

        Object.entries(buttonEvents).forEach(([id, handler]) => {
            if (this.elements[id]) {
                this.elements[id].addEventListener('click', handler);
            }
        });

        // File input
        if (this.elements['file-input']) {
            this.elements['file-input'].addEventListener('change', (e) => this.handleFileImport(e));
        }
    }

    async loadEngines() {
        try {
            this.showEngineLoading(true);
            
            const response = await fetch('/api/models');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.state.engines = data.engines || [];
            this.state.selectedEngine = data.current_engine;
            
            this.renderEngines();
            
        } catch (error) {
            console.error('Failed to load engines:', error);
            this.showError('Failed to load TTS engines');
            this.renderEngineError();
        } finally {
            this.showEngineLoading(false);
        }
    }

    async loadVoices() {
        try {
            this.showVoiceLoading(true);
            
            const response = await fetch('/api/voices');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.state.voices = data.voices || [];
            
            // Auto-select first voice if none selected
            if (this.state.voices.length > 0 && !this.state.selectedVoice) {
                this.state.selectedVoice = this.state.voices[0].id;
            }
            
            this.renderVoices();
            
        } catch (error) {
            console.error('Failed to load voices:', error);
            this.showError('Failed to load voices');
            this.renderVoiceError();
        } finally {
            this.showVoiceLoading(false);
        }
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.state.history = data.history || [];
            
            this.renderHistory();
            this.updateHistoryStats(data.stats || {});
            
        } catch (error) {
            console.error('Failed to load history:', error);
            this.renderHistoryError();
        }
    }

    renderEngines() {
        if (!this.elements['engine-selector']) return;

        if (this.state.engines.length === 0) {
            this.elements['engine-selector'].innerHTML = `
                <div class="no-engines">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>No TTS engines available</p>
                </div>
            `;
            return;
        }

        const engineIcons = {
            'googletts': 'fas fa-globe',
            'google': 'fas fa-globe',
            'coquitts': 'fas fa-brain',
            'coqui': 'fas fa-brain',
            'kittentts': 'fas fa-cat',
            'kitten': 'fas fa-cat',
            'openai': 'fas fa-robot',
            'azure': 'fas fa-cloud',
            'demo': 'fas fa-flask'
        };

        this.elements['engine-selector'].innerHTML = this.state.engines.map(engine => `
            <div class="engine-card ${engine.current ? 'selected' : ''}" data-engine="${engine.id}">
                <div class="engine-icon">
                    <i class="${engineIcons[engine.id] || 'fas fa-robot'}"></i>
                </div>
                <div class="engine-name">${this.escapeHtml(engine.name)}</div>
                <div class="engine-description">${this.escapeHtml(engine.description)}</div>
            </div>
        `).join('');

        // Add click handlers
        this.elements['engine-selector'].querySelectorAll('.engine-card').forEach(card => {
            card.addEventListener('click', () => {
                const engineId = card.dataset.engine;
                this.selectEngine(engineId);
            });
        });
    }

    renderVoices() {
        if (!this.elements['voice-grid']) return;

        if (this.state.voices.length === 0) {
            this.elements['voice-grid'].innerHTML = `
                <div class="no-voices">
                    <i class="fas fa-microphone-slash"></i>
                    <p>No voices available for current engine</p>
                </div>
            `;
            return;
        }

        this.elements['voice-grid'].innerHTML = this.state.voices.map(voice => `
            <div class="voice-card ${voice.id === this.state.selectedVoice ? 'selected' : ''}" data-voice="${voice.id}">
                <div class="voice-name">${this.escapeHtml(voice.name)}</div>
                <div class="voice-gender">${this.escapeHtml(voice.gender || 'Unknown')}</div>
                <div class="voice-description">${this.escapeHtml(voice.description || '')}</div>
            </div>
        `).join('');

        // Add click handlers
        this.elements['voice-grid'].querySelectorAll('.voice-card').forEach(card => {
            card.addEventListener('click', () => {
                const voiceId = card.dataset.voice;
                this.selectVoice(voiceId);
            });
        });
    }

    renderHistory() {
        if (!this.elements['history-list']) return;

        if (this.state.history.length === 0) {
            this.elements['history-list'].innerHTML = `
                <div class="no-history">
                    <i class="fas fa-history"></i>
                    <p data-i18n="no-history">No history yet</p>
                </div>
            `;
            return;
        }

        this.elements['history-list'].innerHTML = this.state.history.map(item => {
            const date = new Date(item.timestamp).toLocaleString();
            const sizeKB = Math.round(item.size / 1024);
            
            return `
                <div class="history-item" data-id="${item.id}">
                    <div class="history-item-text">${this.escapeHtml(item.text)}</div>
                    <div class="history-item-meta">
                        <span>${this.escapeHtml(item.model_type)} • ${this.escapeHtml(item.voice)}</span>
                        <span>${sizeKB}KB • ${date}</span>
                    </div>
                    <div class="history-item-actions">
                        <button class="btn btn-sm btn-outline" onclick="app.playHistoryAudio('${item.id}')" title="Play">
                            <i class="fas fa-play"></i>
                        </button>
                        <button class="btn btn-sm btn-outline" onclick="app.downloadHistoryAudio('${item.id}')" title="Download">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="btn btn-sm btn-danger" onclick="app.deleteHistoryAudio('${item.id}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    async selectEngine(engineId) {
        try {
            const response = await fetch(`/api/models/${engineId}`, {
                method: 'POST'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.state.selectedEngine = data.current_engine;
            
            // Update UI
            this.elements['engine-selector'].querySelectorAll('.engine-card').forEach(card => {
                card.classList.toggle('selected', card.dataset.engine === engineId);
            });
            
            // Reload voices for new engine
            await this.loadVoices();
            
            this.showSuccess(`Switched to ${data.engine_name}`);
            
        } catch (error) {
            console.error('Failed to switch engine:', error);
            this.showError('Failed to switch TTS engine');
        }
    }

    selectVoice(voiceId) {
        this.state.selectedVoice = voiceId;
        
        // Update UI
        this.elements['voice-grid'].querySelectorAll('.voice-card').forEach(card => {
            card.classList.toggle('selected', card.dataset.voice === voiceId);
        });
        
        this.updateGenerateButton();
    }

    handleTextInput() {
        const text = this.elements['text-input']?.value || '';
        const charCount = text.length;
        
        if (this.elements['char-count']) {
            this.elements['char-count'].textContent = charCount;
        }
        
        this.updateGenerateButton();
    }

    updateGenerateButton() {
        if (!this.elements['generate-btn']) return;
        
        const hasText = (this.elements['text-input']?.value || '').trim().length > 0;
        const hasVoice = this.state.selectedVoice !== null;
        const hasEngine = this.state.selectedEngine !== null;
        const canGenerate = hasText && hasVoice && hasEngine && !this.state.isGenerating;
        
        this.elements['generate-btn'].disabled = !canGenerate;
    }

    updateUI() {
        this.updateGenerateButton();
        this.handleTextInput();
    }

    // Utility methods
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showEngineLoading(show) {
        if (!this.elements['engine-selector']) return;
        
        if (show) {
            this.elements['engine-selector'].innerHTML = `
                <div class="loading-engines">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span data-i18n="loading-engines">Loading engines...</span>
                </div>
            `;
        }
    }

    showVoiceLoading(show) {
        if (!this.elements['voice-grid']) return;
        
        if (show) {
            this.elements['voice-grid'].innerHTML = `
                <div class="loading-voices">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span data-i18n="loading-voices">Loading voices...</span>
                </div>
            `;
        }
    }

    renderEngineError() {
        if (!this.elements['engine-selector']) return;
        
        this.elements['engine-selector'].innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load TTS engines</p>
                <button class="btn btn-outline" onclick="app.loadEngines()">Retry</button>
            </div>
        `;
    }

    renderVoiceError() {
        if (!this.elements['voice-grid']) return;
        
        this.elements['voice-grid'].innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load voices</p>
                <button class="btn btn-outline" onclick="app.loadVoices()">Retry</button>
            </div>
        `;
    }

    renderHistoryError() {
        if (!this.elements['history-list']) return;
        
        this.elements['history-list'].innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load history</p>
                <button class="btn btn-outline" onclick="app.loadHistory()">Retry</button>
            </div>
        `;
    }

    showError(message) {
        // Simple error display - can be enhanced with toast notifications
        console.error(message);
        alert(message);
    }

    showSuccess(message) {
        // Simple success display - can be enhanced with toast notifications
        console.log(message);
    }

    // Speech generation
    async generateSpeech() {
        if (this.state.isGenerating) return;

        const text = this.elements['text-input']?.value?.trim();
        if (!text || !this.state.selectedVoice) {
            this.showError('Please enter text and select a voice');
            return;
        }

        try {
            this.state.isGenerating = true;
            this.showProgress(true);
            this.updateGenerateButton();

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    voice: this.state.selectedVoice
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success && data.audio) {
                this.playGeneratedAudio(data.audio);
                this.showDownloadButton(true);
                await this.loadHistory(); // Refresh history
                this.showSuccess('Speech generated successfully!');
            } else {
                throw new Error(data.error || 'Generation failed');
            }

        } catch (error) {
            console.error('Speech generation failed:', error);
            this.showError('Failed to generate speech: ' + error.message);
        } finally {
            this.state.isGenerating = false;
            this.showProgress(false);
            this.updateGenerateButton();
        }
    }

    playGeneratedAudio(audioBase64) {
        try {
            const audioBlob = this.base64ToBlob(audioBase64, 'audio/wav');
            const audioUrl = URL.createObjectURL(audioBlob);

            if (this.elements['audio-player']) {
                this.elements['audio-player'].src = audioUrl;
                this.elements['audio-player'].currentAudioBlob = audioBlob; // Store for download
            }

            if (this.elements['audio-container']) {
                this.elements['audio-container'].style.display = 'block';
            }

        } catch (error) {
            console.error('Failed to play audio:', error);
            this.showError('Failed to play generated audio');
        }
    }

    showProgress(show) {
        if (!this.elements['progress-container']) return;

        if (show) {
            this.elements['progress-container'].style.display = 'block';
            this.animateProgress();
        } else {
            this.elements['progress-container'].style.display = 'none';
            if (this.elements['progress-fill']) {
                this.elements['progress-fill'].style.width = '0%';
            }
        }
    }

    animateProgress() {
        if (!this.elements['progress-fill'] || !this.state.isGenerating) return;

        let progress = 0;
        const interval = setInterval(() => {
            if (!this.state.isGenerating) {
                clearInterval(interval);
                return;
            }

            progress += Math.random() * 15;
            if (progress > 90) progress = 90;

            this.elements['progress-fill'].style.width = progress + '%';
        }, 200);
    }

    showDownloadButton(show) {
        if (this.elements['download-btn']) {
            this.elements['download-btn'].style.display = show ? 'inline-flex' : 'none';
        }
    }

    async downloadAudio() {
        const audioPlayer = this.elements['audio-player'];
        if (!audioPlayer || !audioPlayer.currentAudioBlob) {
            this.showError('No audio to download');
            return;
        }

        try {
            const url = URL.createObjectURL(audioPlayer.currentAudioBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `enhanced_tts_${Date.now()}.wav`;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.showSuccess('Audio downloaded successfully!');
        } catch (error) {
            console.error('Download failed:', error);
            this.showError('Failed to download audio');
        }
    }

    clearText() {
        if (this.elements['text-input']) {
            this.elements['text-input'].value = '';
            this.handleTextInput();
        }
    }

    async handleFileImport(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (file.size > 1024 * 1024) { // 1MB limit
            this.showError('File is too large. Please choose a smaller file.');
            return;
        }

        try {
            const text = await this.readFileAsText(file);
            if (this.elements['text-input']) {
                this.elements['text-input'].value = text;
                this.handleTextInput();
            }
            this.showSuccess('Text imported successfully!');
        } catch (error) {
            console.error('File import failed:', error);
            this.showError('Failed to read file. Please try again.');
        }

        // Clear file input
        event.target.value = '';
    }

    readFileAsText(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = () => reject(new Error('Failed to read file'));
            reader.readAsText(file);
        });
    }

    // Sidebar management
    toggleSidebar() {
        this.state.sidebarOpen = !this.state.sidebarOpen;
        this.updateSidebarState();
    }

    closeSidebar() {
        this.state.sidebarOpen = false;
        this.updateSidebarState();
    }

    updateSidebarState() {
        if (this.elements['sidebar']) {
            this.elements['sidebar'].classList.toggle('open', this.state.sidebarOpen);
        }

        if (this.elements['main-content']) {
            this.elements['main-content'].classList.toggle('sidebar-hidden', !this.state.sidebarOpen);
        }
    }

    // History management
    updateHistoryStats(stats) {
        if (this.elements['total-files']) {
            this.elements['total-files'].textContent = stats.total_files || 0;
        }
        if (this.elements['total-size']) {
            this.elements['total-size'].textContent = (stats.total_size_mb || 0) + ' MB';
        }
    }

    async playHistoryAudio(audioId) {
        try {
            const audioUrl = `/api/history/${audioId}`;
            const audio = new Audio(audioUrl);
            audio.play();
        } catch (error) {
            console.error('Failed to play history audio:', error);
            this.showError('Failed to play audio');
        }
    }

    async downloadHistoryAudio(audioId) {
        try {
            const response = await fetch(`/api/history/${audioId}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `enhanced_tts_${audioId}.wav`;
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            this.showSuccess('Audio downloaded successfully!');
        } catch (error) {
            console.error('Failed to download history audio:', error);
            this.showError('Failed to download audio');
        }
    }

    async deleteHistoryAudio(audioId) {
        if (!confirm('Delete this audio?')) return;

        try {
            const response = await fetch(`/api/history/${audioId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            await this.loadHistory(); // Refresh history
            this.showSuccess('Audio deleted successfully!');
        } catch (error) {
            console.error('Failed to delete history audio:', error);
            this.showError('Failed to delete audio');
        }
    }

    async clearHistory() {
        if (!confirm('Clear all history?')) return;

        try {
            const response = await fetch('/api/history', {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            this.state.history = [];
            this.renderHistory();
            this.updateHistoryStats({ total_files: 0, total_size_mb: 0 });
            this.showSuccess('History cleared successfully!');
        } catch (error) {
            console.error('Failed to clear history:', error);
            this.showError('Failed to clear history');
        }
    }

    // Language toggle
    toggleLanguage() {
        // Simple language toggle - can be enhanced with proper i18n
        const currentLang = this.elements['current-lang']?.textContent || 'EN';
        const newLang = currentLang === 'EN' ? '中文' : 'EN';

        if (this.elements['current-lang']) {
            this.elements['current-lang'].textContent = newLang;
        }

        // Here you would typically trigger i18n updates
        console.log('Language switched to:', newLang);
    }

    // Utility methods
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);

        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new EnhancedTTSApp();
});
