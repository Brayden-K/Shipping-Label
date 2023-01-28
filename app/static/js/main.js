setTimeout(fade_out, 5000);

$(window).ready(function () {
	if (document.location.pathname != '/portal' && document.location.pathname != '/request') {
			try {
				if ($(window).width() < 991) {
				document.getElementById('logo').hidden = false;
				document.getElementById('mobileLogo').hidden = true;
			}
			else {
    			document.getElementById('logo').hidden = true;
    			document.getElementById('mobileLogo').hidden = false;
			}
		} catch(e) {}
	}
});

$(window).resize(function() {
	if (document.location.pathname != '/portal' && document.location.pathname != '/request') {
		if ($(window).width() < 991) {
			document.getElementById('logo').hidden = false;
			document.getElementById('mobileLogo').hidden = true;
		}
		else {
    		document.getElementById('logo').hidden = true;
    		document.getElementById('mobileLogo').hidden = false;
		}
	}
});

function fade_out() {
	try {
		var target = document.getElementById("messages");
		target.remove()
	} catch (e) {}
}

function sendMessage(msg) {
	div = document.createElement('div');
	icon = document.createElement('div');
	icon.innerHTML = '<i class="fa-regular fa-x"></i>';
	icon.setAttribute('onclick', 'fade_out()')
	div.setAttribute('id', 'messages');
	div.classList.add('animate__animated')
	div.classList.add('animate__backInRight')
	div.textContent = msg;
	document.body.appendChild(div);
	div.appendChild(icon);
	setTimeout(fade_out, 10000);
}

function debounce(callback, wait) {
  let timeout;
  return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(function () { callback.apply(this, args); }, wait);
  };
}

function ValidateEmail(input) {
  var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
  if (input.match(validRegex)) {
    return true;
  } else {
    return false;
  }
}

async function updateEmailInput() {
  let emailInput = document.getElementById('registerEmail');
  let emailAvailable = await checkEmailAvailable(emailInput.value);
  if (emailAvailable && ValidateEmail(emailInput.value)) {
    emailInput.setAttribute('style', 'border-color: green !important;');
    return true;
  } else {
    emailInput.setAttribute('style', 'border-color: red !important;');
  }
}

async function checkPasswordsMatch() {
	let passwordInput = document.getElementById('registerPassword');
	let passwordConfirmInput = document.getElementById('registerConfirmPassword');
	if ((passwordInput.value == passwordConfirmInput.value) && passwordInput.value != '') {
		passwordInput.setAttribute('style', 'border-color: green !important;');
		passwordConfirmInput.setAttribute('style', 'border-color: green !important;');
		return true;
	} else {
		passwordInput.setAttribute('style', 'border-color: red !important;');
		passwordConfirmInput.setAttribute('style', 'border-color: red !important;');
	}
}

async function canSubmitSignUp(captcha=false) {
	let passwordInput = document.getElementById('registerPassword');
	if (useCaptcha) {
		if (await checkPasswordsMatch() && await updateEmailInput() && grecaptcha.getResponse() != '') {
			document.getElementById('registerSubmitBtn').disabled = false;
		} else {
			document.getElementById('registerSubmitBtn').disabled = true;
		}
	} else {
		if (await checkPasswordsMatch() && await updateEmailInput()) {
			document.getElementById('registerSubmitBtn').disabled = false;
		} else {
			document.getElementById('registerSubmitBtn').disabled = true;
		}
	}
}

async function captchaRegisterCallback(tes) {
	canSubmitSignUp()
}