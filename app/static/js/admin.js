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

    res = await sendPost(data);
    if (res['success']) {
        sendMessage('Settings have been updated.');
    } else {
        sendMessage('Something went wrong');
    }
}