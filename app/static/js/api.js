async function sendPost(data) {
	const options = {
		method: 'POST',
		headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		body: new URLSearchParams(data)
	};

	return await fetch('/api', options)
		.then(response => response.json())
		.catch(err => console.error(err));
	}

async function createInvoice(price, projectId) {
	let data = {
		'action': 'createInvoice',
		'price': price,
		'projectId': projectId
	};
	res = await sendPost(data);
	if (res['success']) {
		location.href = res['url']
		console.log(res['url'])
	} else {
		if (res['msg'] == 'You already have an active invoice') {
			sendMessage(res['msg'])
			console.log(res['msg'])
			location.href = res['url']
		} else {
			sendMessage('Something went wrong.')
			return {'success': false}
		}
	}
}

async function checkEmailAvailable(email) {
	let data = {
		'action': 'checkEmailAvailable',
		'email': email
	};
	res = await sendPost(data);
	if (res['success'] == true) {
		return true;
	} else {
		return false;
	}
}