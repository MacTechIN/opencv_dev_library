const ws = new WebSocket(`ws://${window.location.host}/ws`);
const logContent = document.getElementById('log-content');
const galleryList = document.getElementById('gallery-list');
const confidenceValue = document.getElementById('confidence-value');
const gaugeProgress = document.getElementById('gauge-progress');
const thresholdDisplay = document.getElementById('threshold-display');
const vectorGrid = document.getElementById('vector-grid');
const detectionBox = document.getElementById('detection-box');
const targetIdLabel = document.getElementById('target-id');

// Initialize Vector Grid (128 cells)
for (let i = 0; i < 64; i++) { // Using 64 for visual density in the smaller box
    const cell = document.createElement('div');
    cell.className = 'bg-primary/10 rounded-sm transition-all duration-300';
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
    const circumference = 264; // Based on r=42 circle
    const offset = circumference - (percent / 100) * circumference;
    gaugeProgress.style.strokeDashoffset = offset;
    confidenceValue.innerText = percent.toFixed(1) + '%';
}

function updateVectorGrid() {
    for (let i = 0; i < 64; i++) {
        const cell = document.getElementById(`v-cell-${i}`);
        const intensity = Math.random();
        cell.style.backgroundColor = `rgba(0, 210, 255, ${intensity})`;
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
            addLog(`${topPerson.id} DETECTED`, 'detected');
            
            people.forEach(p => {
                const card = document.createElement('div');
                card.className = 'flex flex-col items-center gap-3';
                card.innerHTML = `
                    <div class="relative">
                        <div class="w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center border-2 border-primary p-0.5">
                            <span class="material-symbols-outlined text-4xl text-primary/40">person</span>
                        </div>
                        <div class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-success rounded-full border-2 border-charcoal status-pulse"></div>
                    </div>
                    <span class="text-[10px] font-bold text-white/80 font-mono">${p.id}</span>
                `;
                galleryList.appendChild(card);
            });
        } else {
            detectionBox.classList.add('hidden');
        }
    }
};

ws.onopen = () => {
    addLog("WEBSOCKET_CONNECTED", 'online');
};

ws.onclose = () => {
    addLog("WEBSOCKET_DISCONNECTED", 'offline');
};

// UI Listeners
const slider = document.querySelector('input[type="range"]');
if (slider) {
    slider.oninput = (e) => {
        thresholdDisplay.innerText = e.target.value;
    };
}
