let ws;
function connectWS() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        addLog("NETWORK_PROTOCOL [WS] ESTABLISHED", 'online');
        addLog("NEURAL_NET_LOAD_SUCCESSFUL [CORE_V4]", 'info');
    };

    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === 'update') {
            const people = message.data;
            updateDashboard(people);
        } else if (message.type === 'config') {
            // Sync UI with Server State
            const config = message.data;
            if (globalDetectToggle) {
                updateToggleUI(globalDetectToggle, config.global_detect);
            }
            if (autoRegToggle) {
                updateToggleUI(autoRegToggle, config.auto_reg);
            }
            if (slider) {
                slider.value = config.threshold;
                updateSliderUI(config.threshold);
            }
        }
    };

    ws.onclose = () => {
        addLog("WEBSOCKET_DISCONNECTED: Retrying in 2s...", 'offline');
        setTimeout(connectWS, 2000);
    };

    ws.onerror = (err) => {
        console.error("WS Error:", err);
    };
}

function sendCommand(data) {
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: 'command', data: data }));
    }
}

connectWS();
const logContent = document.getElementById('log-content');
const galleryList = document.getElementById('gallery-list');
const confidenceValue = document.getElementById('confidence-value');
const gaugeProgress = document.getElementById('gauge-progress');
const thresholdDisplay = document.getElementById('threshold-display');
const vectorGrid = document.getElementById('vector-grid');

// Initialize Vector Grid
if (vectorGrid) {
    vectorGrid.innerHTML = '';
    for (let i = 0; i < 128; i++) {
        const cell = document.createElement('div');
        cell.className = 'bg-teal-accent/10 rounded-[1px] aspect-square transition-all duration-300';
        cell.id = `v-cell-${i}`;
        vectorGrid.appendChild(cell);
    }
}

function addLog(message, type = '') {
    if (!logContent) return;
    const entry = document.createElement('div');
    entry.className = 'flex gap-4';
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour12: false, fractionalSecondDigits: 3 });
    
    let labelClass = 'text-white/80';
    let msgClass = 'text-white/60';
    
    if (type === 'detected') {
        labelClass = 'text-primary font-bold';
        msgClass = 'text-primary/90';
    } else if (type === 'online') {
        labelClass = 'text-success font-bold';
    } else if (type === 'offline') {
        labelClass = 'text-error font-bold';
    }

    entry.innerHTML = `
        <span class="text-white/20">[${timeStr}]</span>
        <span class="${labelClass}">${type.toUpperCase() || 'INFO'}:</span>
        <span class="${msgClass}">${message}</span>
    `;
    logContent.prepend(entry);
    
    if (logContent.childNodes.length > 50) {
        logContent.removeChild(logContent.lastChild);
    }
}

function updateGauge(percent) {
    if (!gaugeProgress || !confidenceValue) return;
    const circumference = 452.4;
    const offset = circumference - (percent / 100) * circumference;
    gaugeProgress.style.strokeDashoffset = offset;
    confidenceValue.innerText = percent.toFixed(1);
}

function updateVectorGrid() {
    if (!vectorGrid) return;
    for (let i = 0; i < 128; i++) {
        const cell = document.getElementById(`v-cell-${i}`);
        if (!cell) continue;
        const intensity = Math.random();
        const opacity = Math.floor(intensity * 100);
        cell.className = `bg-teal-accent/${opacity} rounded-[1px] aspect-square transition-all duration-300`;
    }
}

function updateDashboard(people) {
    if (!galleryList) return;
    galleryList.innerHTML = '';
    if (people.length > 0) {
        const topPerson = people[0];
        updateGauge(90 + (Math.random() * 8));
        updateVectorGrid();
        addLog(`${topPerson.id} DETECTED`, 'detected');
        
        people.forEach(p => {
            const card = document.createElement('div');
            card.className = 'glass-panel p-4 rounded-2xl flex flex-col items-start gap-4 border-primary/40 bg-primary/5 transition-transform hover:scale-[1.02]';
            card.innerHTML = `
                <div class="relative w-full aspect-square overflow-hidden rounded-xl border border-white/10 bg-black/40">
                    <div class="w-full h-full flex items-center justify-center bg-primary/5">
                        <span class="material-symbols-outlined text-4xl text-primary/20">person</span>
                    </div>
                    <div class="absolute bottom-2 right-2 w-3 h-3 bg-success rounded-full border-2 border-charcoal status-pulse"></div>
                </div>
                <span class="text-[10px] font-bold text-primary font-mono tracking-tight uppercase">${p.id}</span>
            `;
            galleryList.appendChild(card);
        });
    }
}

// System Control Elements
const globalDetectToggle = document.querySelector('[data-control="global_detect"]');
const autoRegToggle = document.querySelector('[data-control="auto_reg"]');
const slider = document.getElementById('threshold-slider');
const thresholdBar = document.getElementById('threshold-bar');
const thresholdThumb = document.getElementById('threshold-thumb');

function updateToggleUI(el, active) {
    if (!el) return;
    const track = el.querySelector('div');
    const thumb = track.querySelector('div');
    if (active) {
        track.classList.remove('bg-white/10');
        track.classList.add('bg-primary/20');
        thumb.classList.remove('left-1', 'bg-white/30');
        thumb.classList.add('right-1', 'bg-primary', 'shadow-[0_0_10px_#00D2FF]');
    } else {
        track.classList.add('bg-white/10');
        track.classList.remove('bg-primary/20');
        thumb.classList.add('left-1', 'bg-white/30');
        thumb.classList.remove('right-1', 'bg-primary', 'shadow-[0_0_10px_#00D2FF]');
    }
}

function updateSliderUI(value) {
    if (!thresholdBar || !thresholdThumb || !thresholdDisplay) return;
    const percent = value * 100;
    thresholdDisplay.innerText = parseFloat(value).toFixed(2);
    thresholdBar.style.width = `${percent}%`;
    thresholdThumb.style.left = `${percent}%`;
}

// Event Listeners
if (globalDetectToggle) {
    globalDetectToggle.onclick = () => {
        const isActive = globalDetectToggle.querySelector('div').classList.contains('bg-primary/20');
        const newState = !isActive;
        updateToggleUI(globalDetectToggle, newState);
        sendCommand({ global_detect: newState });
    };
}

if (autoRegToggle) {
    autoRegToggle.onclick = () => {
        const isActive = autoRegToggle.querySelector('div').classList.contains('bg-primary/20');
        const newState = !isActive;
        updateToggleUI(autoRegToggle, newState);
        sendCommand({ auto_reg: newState });
    };
}

if (slider) {
    slider.oninput = (e) => {
        const value = e.target.value;
        updateSliderUI(value);
        sendCommand({ threshold: value });
    };
}
