async function analyzeSymptoms() {
    const input = document.getElementById('symptomsInput');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    // Get Profile Data
    const age = document.getElementById('ageInput').value;
    const bodyType = document.getElementById('bodyType').value;

    const symptoms = input.value.trim();

    if (!symptoms) {
        alert("Please enter at least one symptom.");
        return;
    }

    // UI Reset
    resultSection.innerHTML = '';
    resultSection.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                symptoms: symptoms,
                profile: {
                    age: age,
                    body_type: bodyType
                }
            })
        });

        const data = await response.json();
        
        // Hide loading
        loading.classList.add('hidden');
        resultSection.classList.remove('hidden');

        if (data.status === 'emergency') {
            renderEmergency(data);
            if (data.lockdown) {
                // UI Lockdown
                input.disabled = true;
                analyzeBtn.disabled = true;
                input.placeholder = "SYSTEM LOCKED - Seek Medical Help";
                analyzeBtn.style.backgroundColor = "#ccc";
            }
        } else if (data.status === 'success') {
            renderDiagnosis(data);
        } else {
            renderUnknown(data);
        }

    } catch (error) {
        console.error('Error:', error);
        loading.classList.add('hidden');
        alert("An error occurred while analyzing symptoms. Please try again.");
    }
}

function renderEmergency(data) {
    const html = `
        <div class="card emergency">
            <h3 class="emergency-title">⚠️ EMERGENCY ALERT</h3>
            <p>${data.message}</p>
            <p><strong>Detected High-Risk Symptoms:</strong> ${data.emergencies.join(', ')}</p>
        </div>
    `;
    document.getElementById('resultSection').innerHTML = html;
}

function renderDiagnosis(data) {
    const severityClass = `severity-${data.severity.toLowerCase()}`;
    
    let remediesHtml = '';
    data.remedies.forEach(remedy => {
        remediesHtml += `
            <li>
                <strong>${remedy.name}</strong><br>
                <small>${remedy.explanation}</small>
            </li>
        `;
    });

    const html = `
        <div class="card">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span class="condition-title">${data.condition}</span>
                <span class="badge ${severityClass}">${data.severity}</span>
            </div>
            
            <h4 style="margin-top: 1.5rem; color: #555;">Recommended Natural Remedies</h4>
            <ul class="remedies-list">
                ${remediesHtml}
            </ul>
        </div>
    `;
    document.getElementById('resultSection').innerHTML = html;
}

function renderUnknown(data) {
    const html = `
        <div class="card">
            <h3 style="color: #666;">Analysis Result</h3>
            <p>${data.message}</p>
        </div>
    `;
    document.getElementById('resultSection').innerHTML = html;
}

// Allow Enter key to submit
document.getElementById('symptomsInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        analyzeSymptoms();
    }
});
