// ===== Text to Speech Studio - Frontend App =====

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // DOM Elements
    const scriptInput = document.getElementById('scriptInput');
    const charCount = document.getElementById('charCount');
    const presetCards = document.getElementById('presetCards');
    const accentGrid = document.getElementById('accentGrid');
    const genderToggle = document.getElementById('genderToggle');
    const emotionPreset = document.getElementById('emotionPreset');
    const speedSlider = document.getElementById('speedSlider');
    const speedValue = document.getElementById('speedValue');
    const musicGrid = document.getElementById('musicGrid');
    const musicVolume = document.getElementById('musicVolume');
    const musicVolumeValue = document.getElementById('musicVolumeValue');
    const generateBtn = document.getElementById('generateBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const outputSection = document.getElementById('outputSection');
    const audioPlayer = document.getElementById('audioPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const regenerateBtn = document.getElementById('regenerateBtn');
    const errorToast = document.getElementById('errorToast');
    const errorMessage = document.getElementById('errorMessage');
    const settingsSummary = document.getElementById('settingsSummary');

    // Summary elements
    const summaryPreset = document.getElementById('summaryPreset');
    const summaryEmotion = document.getElementById('summaryEmotion');
    const summaryAccent = document.getElementById('summaryAccent');
    const summarySpeed = document.getElementById('summarySpeed');
    const summaryMusic = document.getElementById('summaryMusic');

    let currentDownloadUrl = '';
    let currentPreviewUrl = '';
    let selectedPreset = 'storyteller';
    let selectedAccent = 'us';
    let selectedGender = 'male';
    let selectedMusic = 'none';
    let presetsData = {};
    let accentsData = {};
    let emotionsData = {};
    let musicData = {};

    // ===== Character Counter =====
    scriptInput.addEventListener('input', function() {
        const len = this.value.length;
        charCount.textContent = `${len} / 10000`;
        if (len > 9000) {
            charCount.style.color = 'var(--accent-orange)';
        } else if (len > 9500) {
            charCount.style.color = 'var(--accent-red)';
        } else {
            charCount.style.color = '';
        }
    });

    // ===== Speed Slider =====
    speedSlider.addEventListener('input', function() {
        speedValue.textContent = `${parseFloat(this.value).toFixed(1)}x`;
        updateSummary();
    });

    // ===== Music Volume Slider =====
    musicVolume.addEventListener('input', function() {
        musicVolumeValue.textContent = `${this.value}%`;
    });

    // ===== Update Settings Summary =====
    function updateSummary() {
        // Preset
        if (presetsData[selectedPreset]) {
            summaryPreset.textContent = presetsData[selectedPreset].label;
        }
        // Emotion
        const emotionOpt = emotionPreset.options[emotionPreset.selectedIndex];
        summaryEmotion.textContent = emotionOpt.textContent;
        // Accent
        if (accentsData[selectedAccent]) {
            summaryAccent.textContent = accentsData[selectedAccent].label;
        }
        // Speed
        summarySpeed.textContent = `${parseFloat(speedSlider.value).toFixed(1)}x`;
        // Music
        if (musicData[selectedMusic]) {
            summaryMusic.textContent = musicData[selectedMusic].label;
        }
    }

    // ===== Load Options from Server =====
    async function loadOptions() {
        try {
            const response = await fetch('/api/voice-presets');
            const data = await response.json();
            
            presetsData = data.presets;
            accentsData = data.accents;
            emotionsData = data.emotions;
            musicData = data.music_categories;

            // Render preset cards
            renderPresetCards(data.presets);
            
            // Render accent cards
            renderAccentCards(data.accents);
            
            // Render music cards
            renderMusicCards(data.music_categories);
            
            // Update summary
            updateSummary();
            
        } catch (err) {
            console.log('Could not load options:', err.message);
        }
    }

    // ===== Render Preset Cards =====
    function renderPresetCards(presets) {
        presetCards.innerHTML = '';
        Object.entries(presets).forEach(([key, preset]) => {
            const card = document.createElement('div');
            card.className = `preset-card${key === selectedPreset ? ' active' : ''}`;
            card.dataset.preset = key;
            card.innerHTML = `
                <span class="preset-label">${preset.label}</span>
                <span class="preset-desc">${preset.desc || ''}</span>
            `;
            card.addEventListener('click', function() {
                // Remove active from all
                document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedPreset = this.dataset.preset;
                updateSummary();
            });
            presetCards.appendChild(card);
        });
    }

    // ===== Render Accent Cards =====
    function renderAccentCards(accents) {
        accentGrid.innerHTML = '';
        Object.entries(accents).forEach(([key, accent]) => {
            const card = document.createElement('div');
            card.className = `accent-card${key === selectedAccent ? ' active' : ''}`;
            card.dataset.accent = key;
            card.innerHTML = `
                <span class="accent-flag">${accent.flag || '🌐'}</span>
                <span class="accent-label">${accent.label.replace(/^.{1,2}\s/, '') || key.toUpperCase()}</span>
            `;
            card.addEventListener('click', function() {
                document.querySelectorAll('.accent-card').forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                selectedAccent = this.dataset.accent;
                updateSummary();
            });
            accentGrid.appendChild(card);
        });
    }

    // ===== Gender Toggle =====
    genderToggle.addEventListener('click', function(e) {
        const btn = e.target.closest('.gender-btn');
        if (!btn) return;
        
        document.querySelectorAll('.gender-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedGender = btn.dataset.gender;
    });

    // ===== Emotion Change =====
    emotionPreset.addEventListener('change', function() {
        updateSummary();
    });

    // ===== Render Music Cards =====
    function renderMusicCards(musicOptions) {
        musicGrid.innerHTML = '';
        Object.entries(musicOptions).forEach(([key, music]) => {
            const card = document.createElement('div');
            card.className = `music-card${key === selectedMusic ? ' active' : ''}${!music.available ? ' unavailable' : ''}`;
            card.dataset.music = key;
            
            let badge = '';
            if (key === 'none') {
                badge = '<span class="music-badge">Default</span>';
            } else if (music.available) {
                badge = '<span class="music-badge">✓ Ready</span>';
            } else {
                badge = '<span class="music-badge">⬇ Add file</span>';
            }
            
            card.innerHTML = `
                <span class="music-icon">${music.icon || '🎵'}</span>
                <span class="music-label">${music.label.replace(/^.{1,2}\s/, '') || key}</span>
                ${badge}
            `;
            
            if (music.available || key === 'none') {
                card.addEventListener('click', function() {
                    document.querySelectorAll('.music-card').forEach(c => c.classList.remove('active'));
                    this.classList.add('active');
                    selectedMusic = this.dataset.music;
                    updateSummary();
                });
            }
            
            musicGrid.appendChild(card);
        });
    }

    // ===== Generate Audio =====
    generateBtn.addEventListener('click', async function() {
        const script = scriptInput.value.trim();
        
        if (!script) {
            showError('Please paste your script first!');
            scriptInput.focus();
            return;
        }

        if (script.length < 10) {
            showError('Script is too short. Please write at least 10 characters.');
            return;
        }

        // Disable button and show loading
        generateBtn.disabled = true;
        generateBtn.innerHTML = '⏳ Generating...';
        loadingIndicator.classList.remove('hidden');
        outputSection.classList.add('hidden');

        try {
            const payload = {
                script: script,
                preset: selectedPreset,
                accent: selectedAccent,
                gender: selectedGender,
                emotion: emotionPreset.value,
                speed: parseFloat(speedSlider.value),
                music_category: selectedMusic,
                music_volume: parseInt(musicVolume.value)
            };

            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Generation failed');
            }

            // Success - show output
            currentPreviewUrl = result.preview_url;
            currentDownloadUrl = result.download_url;

            audioPlayer.src = currentPreviewUrl;
            audioPlayer.load();

            downloadBtn.onclick = function() {
                if (currentDownloadUrl) {
                    window.location.href = currentDownloadUrl;
                }
            };

            outputSection.classList.remove('hidden');
            
            audioPlayer.play().catch(() => {});

        } catch (err) {
            showError(err.message || 'An error occurred during generation');
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<span class="btn-icon">🔊</span> Generate Audio';
            loadingIndicator.classList.add('hidden');
        }
    });

    // ===== Regenerate =====
    regenerateBtn.addEventListener('click', function() {
        outputSection.classList.add('hidden');
        audioPlayer.src = '';
        scriptInput.focus();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ===== Keyboard shortcuts =====
    scriptInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            generateBtn.click();
        }
    });

    // ===== Toast Error =====
    function showError(msg) {
        errorMessage.textContent = msg;
        errorToast.classList.remove('hidden');
        
        if (window.toastTimeout) {
            clearTimeout(window.toastTimeout);
        }
        window.toastTimeout = setTimeout(() => {
            errorToast.classList.add('hidden');
        }, 5000);
    }

    window.closeToast = function() {
        errorToast.classList.add('hidden');
        if (window.toastTimeout) {
            clearTimeout(window.toastTimeout);
        }
    };

    // ===== Handle paste events =====
    scriptInput.addEventListener('paste', function() {
        setTimeout(() => {
            const len = this.value.length;
            if (len > 9500) {
                showError('Script is very long! Maximum is 10000 characters.');
            }
        }, 50);
    });

    // ===== Initialize =====
    loadOptions();
    console.log('🎙️ Text to Speech Studio loaded successfully!');
    console.log('💡 Tip: Click preset cards, choose accent & gender, then Generate!');
});