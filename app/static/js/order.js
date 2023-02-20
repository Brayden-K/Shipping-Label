$(document).ready(
function()
    {
        $(".providerBtn").click(async function(event) {
        	$(".providerBtn").removeClass("active");
        	$(this).addClass("active");
        	let providerId = document.getElementsByClassName('active')[0].id.split('-')[1];
        	let data = {
				'action': 'getServices',
				'id': providerId,
			};
			res = await sendPost(data);
			if (res['success']) {
				let serviceContainer = document.getElementById('services');
				serviceContainer.innerHTML = "";
				serviceContainer.hidden = false;
				let serviceRow = document.createElement('div');
				serviceRow.classList.add('row');
				serviceContainer.appendChild(serviceRow);
				res['services'].forEach(service => {
					let x = document.createElement('div');
					x.classList.add('col-md-4');
					x.classList.add('text-center');
					x.innerHTML = `<div class="card service" onclick="setServiceId(${service.id}, this)"><span class="serviceName"><small>${service.name}</small></span><span class="servicePrice">$${service.price}</span></div>`;
					serviceRow.appendChild(x);
				})
			}
        }
    );
});
async function setServiceId(serviceId, element) {
	window.serviceId = serviceId;
	document.getElementById('shippingForm').hidden = false;
	$(".service").removeClass("activeService");
	$(".service").hide();
	$(element).addClass("activeService");
	$(element).parent().removeClass("col-md-4");
	$(element).parent().addClass("col-md-12");
	$(element).show();
}

async function setupToTemplate(element) {
	let toaddress1 = document.getElementById('toaddress1');
	let toaddress2 = document.getElementById('toaddress2');
	let toaddress3 = document.getElementById('toaddress3');
	let tocity = document.getElementById('tocity');
	let tostate = document.getElementById('tostate');
	let topostalCode = document.getElementById('topostalCode');
	let tocompanyName = document.getElementById('tocompanyName');
	let tophone = document.getElementById('tophone');
	let tocountry = document.getElementById('tocountry');
	if (!element) {
		console.log(element)
		return;
	}

	if (element == 'No Template') {
		toaddress1.value = "";
		toaddress2.value = "";
		toaddress3.value = "";
		tocity.value = "";
		tostate.value = "";
		topostalCode.value = "";
		tocompanyName.value = "";
		tophone.value = "";
		tocountry.value = "";
		return;
	}

	let data = {
		'action': 'getTemplate',
		'id': element,
	};
	res = await sendPost(data);
	if (res['success']) {
		toaddress1.value = res['template']['address1'];
		toaddress2.value = res['template']['address2'];
		toaddress3.value = res['template']['address3'];
		tocity.value = res['template']['city'];
		tostate.value = res['template']['state'];
		topostalCode.value = res['template']['postalCode'];
		tocompanyName.value = res['template']['companyName'];
		tophone.value = res['template']['phone'];
		tocountry.value = res['template']['country'];
		return;
	}
}

async function setupFromTemplate(element) {
	let fromaddress1 = document.getElementById('fromaddress1');
	let fromaddress2 = document.getElementById('fromaddress2');
	let fromaddress3 = document.getElementById('fromaddress3');
	let fromcity = document.getElementById('fromcity');
	let fromstate = document.getElementById('fromstate');
	let frompostalCode = document.getElementById('frompostalCode');
	let fromcompanyName = document.getElementById('fromcompanyName');
	let fromphone = document.getElementById('fromphone');
	let fromcountry = document.getElementById('fromcountry');
	if (!element) {
		console.log(element)
		return;
	}

	if (element == 'No Template') {
		fromaddress1.value = "";
		fromaddress2.value = "";
		fromaddress3.value = "";
		fromcity.value = "";
		fromstate.value = "";
		frompostalCode.value = "";
		fromcompanyName.value = "";
		fromphone.value = "";
		fromcountry.value = "";
		return;
	}

	let data = {
		'action': 'getTemplate',
		'id': element,
	};
	res = await sendPost(data);
	if (res['success']) {
		fromaddress1.value = res['template']['address1'];
		fromaddress2.value = res['template']['address2'];
		fromaddress3.value = res['template']['address3'];
		fromcity.value = res['template']['city'];
		fromstate.value = res['template']['state'];
		frompostalCode.value = res['template']['postalCode'];
		fromcompanyName.value = res['template']['companyName'];
		fromphone.value = res['template']['phone'];
		fromcountry.value = res['template']['country'];
		return;
	}
}

document.getElementById('createLabelBtn').addEventListener("click", async function(){
    const variables = ['toaddress1', 'tocity', 'tostate', 'topostalCode', 'tocountry', 'fromaddress1', 'fromcity', 'fromstate', 'frompostalCode', 'fromcountry'];
	for (let variable of variables) {
		if (!document.getElementById(variable).value) {
			sendMessage('Please fill out the required fields.')
			console.log(variable)
			return;
		}
	}
	createLabel();
});

async function createLabel() {
	console.log(window.serviceId);
}