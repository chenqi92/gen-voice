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
        'voice-male': 'Male',
        'engine-title': 'TTS Engine',
        'engine-description': 'Choose your preferred text-to-speech engine',
        'loading-engines': 'Loading engines...',
        'voice-title': 'Voice Selection',
        'voice-description': 'Select a voice that suits your needs',
        'loading-voices': 'Loading voices...',
        'input-title': 'Text Input',
        'input-description': 'Enter the text you want to convert to speech',
        'input-placeholder': 'Enter your text here...',
        'audio-title': 'Generated Audio',
        'audio-not-supported': 'Your browser does not support the audio element.',
        'history-title': 'History',
        'loading-history': 'Loading history...',
        'no-history': 'No history yet',
        'total-files': 'Total Files',
        'total-size': 'Total Size',
        'refresh': 'Refresh',
        'clear-all': 'Clear All',
        'history': 'History',
        'about-title': 'About Enhanced TTS',
        'about-description': 'Advanced AI-powered text-to-speech system with multiple engines and voice options.',
        'features-title': 'Features',
        'feature-1': 'Multiple TTS Engines',
        'feature-2': 'High-Quality Voices',
        'feature-3': 'History Management',
        'feature-4': 'Real-time Generation',
        'support-title': 'Support',
        'support-description': 'For technical support and feature requests, please contact our team.',
        'rights-reserved': 'All rights reserved.',
        'confirm-delete': 'Delete this audio?',
        'confirm-clear-all': 'Clear all history?'
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
        'voice-male': '男声',
        'engine-title': 'TTS引擎',
        'engine-description': '选择您偏好的文本转语音引擎',
        'loading-engines': '正在加载引擎...',
        'voice-title': '声音选择',
        'voice-description': '选择适合您需求的声音',
        'loading-voices': '正在加载声音...',
        'input-title': '文本输入',
        'input-description': '输入您想要转换为语音的文本',
        'input-placeholder': '在此输入您的文本...',
        'audio-title': '生成的音频',
        'audio-not-supported': '您的浏览器不支持音频元素。',
        'history-title': '历史记录',
        'loading-history': '正在加载历史...',
        'no-history': '暂无历史记录',
        'total-files': '总文件数',
        'total-size': '总大小',
        'refresh': '刷新',
        'clear-all': '清空全部',
        'history': '历史记录',
        'about-title': '关于增强TTS',
        'about-description': '先进的AI驱动文本转语音系统，支持多种引擎和声音选项。',
        'features-title': '功能特性',
        'feature-1': '多种TTS引擎',
        'feature-2': '高质量声音',
        'feature-3': '历史记录管理',
        'feature-4': '实时生成',
        'support-title': '技术支持',
        'support-description': '如需技术支持和功能请求，请联系我们的团队。',
        'rights-reserved': '版权所有。',
        'confirm-delete': '删除此音频？',
        'confirm-clear-all': '清空所有历史记录？'
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
