// Internationalization (i18n) support
const translations = {
    en: {
        'nav-subtitle': 'High-quality AI voice generation',
        'input-title': 'Enter Your Text',
        'input-placeholder': 'Type your text here or import a text file...',
        'import-btn': 'Import Text File',
        'clear-btn': 'Clear',
        'characters': 'characters',
        'voice-title': 'Choose Voice',
        'loading-voices': 'Loading voices...',
        'generate-btn': 'Generate Speech',
        'download-btn': 'Download Audio',
        'features-title': 'Features',
        'feature-cpu-title': 'CPU Only',
        'feature-cpu-desc': 'Runs entirely on CPU without requiring expensive GPUs',
        'feature-lightweight-title': 'Lightweight',
        'feature-lightweight-desc': 'Only 25MB model size with 15M parameters',
        'feature-voices-title': 'Multiple Voices',
        'feature-voices-desc': '8 expressive voices with different characteristics',
        'feature-fast-title': 'Ultra Fast',
        'feature-fast-desc': 'Real-time speech generation for responsive applications',
        'feature-opensource-title': 'Open Source',
        'feature-opensource-desc': 'Apache 2.0 license for commercial and personal use',
        'feature-privacy-title': 'Privacy First',
        'feature-privacy-desc': 'All processing happens locally, no data sent to servers',
        'footer-text': 'Built with ❤️ for the open source community.',
        'generating': 'Generating speech...',
        'error-empty-text': 'Please enter some text to generate speech.',
        'error-no-voice': 'Please select a voice.',
        'error-generation': 'Failed to generate speech. Please try again.',
        'success-generated': 'Speech generated successfully!',
        'downloading': 'Preparing download...',
        'error-download': 'Failed to download audio. Please try again.',
        'error-file-read': 'Failed to read file. Please try again.',
        'error-file-size': 'File is too large. Please choose a smaller file.',
        'success-imported': 'Text imported successfully!',
        'voice-female': 'Female',
        'voice-male': 'Male'
    },
    zh: {
        'nav-subtitle': '高质量AI语音生成',
        'input-title': '输入文本',
        'input-placeholder': '在此输入您的文本或导入文本文件...',
        'import-btn': '导入文本文件',
        'clear-btn': '清空',
        'characters': '个字符',
        'voice-title': '选择声音',
        'loading-voices': '正在加载声音...',
        'generate-btn': '生成语音',
        'download-btn': '下载音频',
        'features-title': '功能特色',
        'feature-cpu-title': '仅需CPU',
        'feature-cpu-desc': '完全在CPU上运行，无需昂贵的GPU',
        'feature-lightweight-title': '轻量级',
        'feature-lightweight-desc': '仅25MB模型大小，1500万参数',
        'feature-voices-title': '多种声音',
        'feature-voices-desc': '8种富有表现力的不同特色声音',
        'feature-fast-title': '超快速度',
        'feature-fast-desc': '实时语音生成，响应迅速的应用体验',
        'feature-opensource-title': '开源',
        'feature-opensource-desc': 'Apache 2.0许可证，支持商业和个人使用',
        'feature-privacy-title': '隐私优先',
        'feature-privacy-desc': '所有处理都在本地进行，不向服务器发送数据',
        'footer-text': '用❤️为开源社区构建。',
        'generating': '正在生成语音...',
        'error-empty-text': '请输入一些文本来生成语音。',
        'error-no-voice': '请选择一个声音。',
        'error-generation': '生成语音失败，请重试。',
        'success-generated': '语音生成成功！',
        'downloading': '正在准备下载...',
        'error-download': '下载音频失败，请重试。',
        'error-file-read': '读取文件失败，请重试。',
        'error-file-size': '文件过大，请选择较小的文件。',
        'success-imported': '文本导入成功！',
        'voice-female': '女声',
        'voice-male': '男声'
    }
};

class I18n {
    constructor() {
        this.currentLang = localStorage.getItem('kitten-tts-lang') || 'en';
        this.init();
    }

    init() {
        // Set up language toggle buttons
        const langButtons = document.querySelectorAll('.lang-btn');
        langButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const lang = e.target.id.split('-')[1];
                this.setLanguage(lang);
            });
        });

        // Apply initial language
        this.applyLanguage();
    }

    setLanguage(lang) {
        if (lang === this.currentLang) return;
        
        this.currentLang = lang;
        localStorage.setItem('kitten-tts-lang', lang);
        
        // Update button states
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`lang-${lang}`).classList.add('active');
        
        this.applyLanguage();
    }

    applyLanguage() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        });

        // Handle placeholder attributes
        const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
        placeholderElements.forEach(element => {
            const key = element.getAttribute('data-i18n-placeholder');
            const translation = this.getTranslation(key);
            if (translation) {
                element.placeholder = translation;
            }
        });

        // Update active language button
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`lang-${this.currentLang}`).classList.add('active');
    }

    getTranslation(key) {
        return translations[this.currentLang]?.[key] || translations.en[key] || key;
    }

    t(key) {
        return this.getTranslation(key);
    }
}

// Initialize i18n when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.i18n = new I18n();
});
