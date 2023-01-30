document.getElementById('registerEmail').addEventListener('keyup', debounce( () => {
    updateEmailInput();
    canSubmitSignUp();
}, 1000))

document.getElementById('registerConfirmPassword').addEventListener('keyup', debounce( () => {
    checkPasswordsMatch();
    canSubmitSignUp();
}, 1000))

try {
    document.getElementById("msgBClose").addEventListener("click", function(){
        document.getElementById('alert-dashboard-message').remove()
    });
} catch (e) {
    
}

