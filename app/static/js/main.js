setTimeout(fade_out, 5000);

$(document).ready(function () {
    $('#TemplateTable').DataTable({
        responsive: true,
    });
});

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

async function viewTemplate(id) {
	let name = document.getElementById('editname');
	let address1 = document.getElementById('editaddress1');
	let type = document.getElementById('edittype');
	let address2 = document.getElementById('editaddress2');
	let address3 = document.getElementById('editaddress3');
	let city = document.getElementById('editcity');
	let state = document.getElementById('editstate');
	let postalCode = document.getElementById('editpostalCode');
	let companyName = document.getElementById('editcompanyName');
	let phone = document.getElementById('editphone');
	let country = document.getElementById('editcountry');
	let idInput = document.getElementById('idEditInput');
	$('#deleteTemplateBtn').click(function(){
	  location.href = `${window.location.protocol}//${window.location.host}/deleteTemplate?id=${id}`;
	});
	var editTemplate = new bootstrap.Modal(document.getElementById('editTemplate'), {
  	keyboard: true,
  	focus: true,
  	backdrop: true
	});
	data = {'action': 'getTemplate', 'id': id}
	res = await sendPost(data);
  if (res['success']) {
  	name.value = res['template']['name'];
  	idInput.value = id;
		address1.value = res['template']['address1'];
		address2.value = res['template']['address2'];
		address3.value = res['template']['address3'];
		city.value = res['template']['city'];
		state.value = res['template']['state'];
		postalCode.value = res['template']['postalCode'];
		companyName.value = res['template']['companyName'];
		phone.value = res['template']['phone'];
		type.placeholder = res['template']['type'];
		type.value = res['template']['type'];
		country.placeholder = res['template']['country'];
		country.value = res['template']['country']
    editTemplate.show()
  } else {
      sendMessage('You do not own this template.');
  }
}

async function changePassword() {
	let submitBtn = document.getElementById('changePasswordSubmitBtn');
	data = {
			'action': 'changePassword',
			'currentPassword': document.getElementById('currentPassword').value,
			'newPassword': document.getElementById('newPassword').value,
			'newRepeatPassword': document.getElementById('newRepeatPassword').value,
		}
	res = await sendPost(data);
  if (res['success']) {
  	sendMessage('Password has been changed');
  	document.getElementById('currentPassword').value = '';
		document.getElementById('newPassword').value = '';
		document.getElementById('newRepeatPassword').value = '';
  	$('#changePasswordModal').modal('hide');
  } else {
  	sendMessage(res['msg']);
  }
}

async function saveUserSettings() {
	let submitBtn = document.getElementById('changePasswordSubmitBtn');
	data = {
			'action': 'saveUserSettings',
			'email': document.getElementById('editEmail').value,
			'discord': document.getElementById('editDiscord').value,
			'telegram': document.getElementById('editTelegram').value,
		}
	res = await sendPost(data);
  if (res['success']) {
  	sendMessage('User settings have been updated.');
  	$('#userSettingsModal').modal('hide');
  } else {
  	sendMessage(res['msg']);
  }
}