document.getElementById('showDashboardMessage').addEventListener('change', function(e) {
    if (document.getElementById('showDashboardMessage').checked) {
        let title = document.getElementById('dashboardTitle');
        let message = document.getElementById('dashboardMessage');
        title.disabled = false;
        message.disabled = false;
    } else {
        let title = document.getElementById('dashboardTitle');
        let message = document.getElementById('dashboardMessage');
        title.disabled = true;
        message.disabled = true;
    }
});

document.getElementById("saveSettingsBtn").addEventListener("click", function(){
    saveSettings();
});

document.getElementById("saveUserSettingsBtn").addEventListener("click", function(){
    saveSettings();
});

async function saveSettings() {
    let data = {};
    data['action'] = 'updateSettings';
    data['siteName'] = document.getElementById('siteName').value;
    data['siteTitle'] = document.getElementById('siteTitle').value;
    data['siteDescription'] = document.getElementById('siteDescription').value;
    data['underConstruction'] = document.getElementById('underConstruction').checked;
    data['requireCaptcha'] = document.getElementById('requireCaptcha').checked;
    data['showDashboardMessage'] = document.getElementById('showDashboardMessage').checked;
    data['dashboardTitle'] = document.getElementById('dashboardTitle').value;
    data['dashboardMessage'] = document.getElementById('dashboardMessage').value;
    data['upsApiKey'] = document.getElementById('upsApiKey').value;
    data['fedexApiKey'] = document.getElementById('fedexApiKey').value;
    data['uspsApiKey'] = document.getElementById('uspsApiKey').value;

    res = await sendPost(data);
    if (res['success']) {
        sendMessage('Settings have been updated.');
    } else {
        sendMessage('Something went wrong');
    }
}

function fixRange(id) {
    let progressSlider = document.getElementById(`progressSlider${id}`);
    let progressBar = document.getElementById(`progress${id}`);
    progressBar.innerHTML = `${progressSlider.value}%`;
    progressBar.style.width = progressSlider.value + '%';
}

async function updateProgress(id) {
    let data = {};
    ticketProgress = document.getElementById(`progressSlider${id}`);
    data['action'] = 'updateTicket';
    data['id'] = id;
    data['progress'] = ticketProgress.value
    res = await sendPost(data);
    if (res['success']) {
        sendMessage('Ticket has been updated.');
    } else {
        sendMessage('Something went wrong');
    }
}

async function updateTicketComplete(complete, id) {
    let data = {};
    data['action'] = 'updateTicket';
    data['id'] = id;
    data['complete'] = complete
    res = await sendPost(data);
    if (res['success']) {
        sendMessage('Ticket has been updated.');
        let completeIcon = document.getElementById(`completeIcon${id}`);
        if (complete == 0) {
            completeIcon.classList.remove('fa-check');
            completeIcon.classList.remove('text-success')
            completeIcon.classList.add('fa-x')
            completeIcon.classList.add('text-danger')
        } else {
            completeIcon.classList.add('fa-check');
            completeIcon.classList.add('text-success')
            completeIcon.classList.remove('fa-x')
            completeIcon.classList.remove('text-danger')
        }
    } else {
        sendMessage('Something went wrong');
    }
}