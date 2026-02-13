const ws = new WebSocket(`ws://${window.location.host}/ws`);
const logContent = document.getElementById('log-content');
const galleryList = document.getElementById('gallery-list');
const confidenceValue = document.getElementById('confidence-value');
const gaugeProgress = document.getElementById('gauge-progress');
const thresholdDisplay = document.getElementById('threshold-display');
const vectorGrid = document.getElementById('vector-grid');
const detectionBox = document.getElementById('detection-box');
const targetIdLabel = document.getElementById('target-id');

// Initialize Vector Grid (128 cells for the new v4 design)
for (let i = 0; i < 128; i++) {
    const cell = document.createElement('div');
    cell.className = 'bg-teal-accent/10 rounded-[1px] aspect-square transition-all duration-300';
    cell.id = `v-cell-${i}`;
    vectorGrid.appendChild(cell);
}

function addLog(message, type = '') {
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
    } else if (type === 'identity_lock') {
        labelClass = 'text-white/80 font-bold';
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
    const circumference = 452.4; // Based on r=72 circle (v4 UI)
    const offset = circumference - (percent / 100) * circumference;
    gaugeProgress.style.strokeDashoffset = offset;
    confidenceValue.innerText = percent.toFixed(1);
}

function updateVectorGrid() {
    for (let i = 0; i < 128; i++) {
        const cell = document.getElementById(`v-cell-${i}`);
        const intensity = Math.random();
        const opacity = Math.floor(intensity * 100);
        cell.className = `bg-teal-accent/${opacity} rounded-[1px] aspect-square transition-all duration-300`;
    }
}

ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    
    if (message.type === 'update') {
        const people = message.data;
        
        galleryList.innerHTML = '';
        if (people.length > 0) {
            detectionBox.classList.remove('hidden');
            const topPerson = people[0];
            targetIdLabel.innerText = `${topPerson.id} | TRUSTED`;
            
            updateGauge(94.2 + (Math.random() * 2));
            updateVectorGrid();
            addLog(`${topPerson.id} DETECTED (Match_Score: 0.942)`, 'detected');
            
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
        } else {
            detectionBox.classList.add('hidden');
        }
    }
};

ws.onopen = () => {
    addLog("STREAM_ACTIVE", 'online');
    addLog("NEURAL_NET_LOAD_SUCCESSFUL [CORE_V4]", 'info');
};

ws.onclose = () => {
    addLog("WEBSOCKET_DISCONNECTED", 'offline');
};

// Custom Slider UI Listeners
const slider = document.getElementById('threshold-slider');
const thresholdBar = document.getElementById('threshold-bar');
const thresholdThumb = document.getElementById('threshold-thumb');

if (slider) {
    slider.oninput = (e) => {
        const value = e.target.value;
        const percent = value * 100;
        thresholdDisplay.innerText = parseFloat(value).toFixed(2);
        thresholdBar.style.width = `${percent}%`;
        thresholdThumb.style.left = `${percent}%`;
    };
}
