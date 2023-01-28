document.getElementById('registerEmail').addEventListener('keyup', debounce( () => {
    updateEmailInput();
    canSubmitSignUp();
}, 1000))

document.getElementById('registerConfirmPassword').addEventListener('keyup', debounce( () => {
    checkPasswordsMatch();
    canSubmitSignUp();
}, 1000))