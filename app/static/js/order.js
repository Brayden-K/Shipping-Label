$(document).ready(
function()
    {
        $(".providerBtn").click(async function(event) {
        	$(".providerBtn").removeClass("active");
        	$(this).addClass("active");
        	window.providerId = parseInt(this.id.split('-')[1]);
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
					if (service.ca) {
						x.innerHTML = `<div class="card service" onclick="setServiceId(${service.id}, this)"><span class="serviceName"><small>${service.name}</small></span><span class="servicePrice">$${service.price}</span><span class="small">Canada</span></div>`;
					} else {
						x.innerHTML = `<div class="card service" onclick="setServiceId(${service.id}, this)"><span class="serviceName"><small>${service.name}</small></span><span class="servicePrice">$${service.price}</span></div>`;
					}
					serviceRow.appendChild(x);
				})
			}
        }
    );
});

$(document).ready(function () {
    $('#orderTable').DataTable({
        responsive: true,
        order: [[2, 'desc']],
    });
});

async function setServiceId(serviceId, element) {
	window.serviceId = serviceId;
	let container = document.getElementById('extraOptions');
	if (serviceId == 1) {
		extraOptions.innerHTML = `<div class="form-check">
							<label class="form-check-label" for="signature">
								Signature Required
							</label>
							<input class="form-check-input" type="checkbox" value="" id="signature">
						</div>
						<div class="form-check">
							<label class="form-check-label" for="saturday">
								Saturday Delivery
							</label>
							<input class="form-check-input" type="checkbox" value="" id="saturday">
						</div>`;
	} else {
		extraOptions.innerHTML = '';
	}
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

if (document.getElementById('createLabelBtn')) {
	document.getElementById('createLabelBtn').addEventListener("click", async function(){
		if (window.providerId == 1) {
	    	const variables = ['fromcompanyName', 'tocompanyName', 'tophone', 'fromphone', 'toaddress1', 'tocity', 'tostate', 'topostalCode', 'tocountry', 'fromaddress1', 'fromcity', 'fromstate', 'frompostalCode', 'fromcountry', 'formlength', 'formwidth', 'formheight', 'formweight'];
			for (let variable of variables) {
				if (!document.getElementById(variable).value) {
					sendMessage('Please fill out the required fields.')
					console.log(variable)
					return;
				}
			}
			sendMessage('Creating your label now. Please wait.')
			createLabel();
		} else if (window.providerId == 2 || window.providerId == 3) {
			const variables = ['toaddress1', 'tocity', 'tostate', 'topostalCode', 'tocountry', 'fromaddress1', 'fromcity', 'fromstate', 'frompostalCode', 'fromcountry', 'formlength', 'formwidth', 'formheight', 'formweight'];
			for (let variable of variables) {
				if (!document.getElementById(variable).value) {
					sendMessage('Please fill out the required fields.')
					console.log(variable)
					return;
				}
			}
			sendMessage('Creating your label now. Please wait.')
			createLabel();
		}
	});
}

async function createLabel() {
	let labelBtn = document.getElementById('createLabelBtn');
	labelBtn.innerHTML = '<span class="spinner-border"></span>'
	labelBtn.disabled = true;
	let toaddress1 = document.getElementById('toaddress1');
	let toaddress2 = document.getElementById('toaddress2');
	let toaddress3 = document.getElementById('toaddress3');
	let tocity = document.getElementById('tocity');
	let tostate = document.getElementById('tostate');
	let topostalCode = document.getElementById('topostalCode');
	let tocompanyName = document.getElementById('tocompanyName');
	let tophone = document.getElementById('tophone');
	let tocountry = document.getElementById('tocountry');
	let fromaddress1 = document.getElementById('fromaddress1');
	let fromaddress2 = document.getElementById('fromaddress2');
	let fromaddress3 = document.getElementById('fromaddress3');
	let fromcity = document.getElementById('fromcity');
	let fromstate = document.getElementById('fromstate');
	let frompostalCode = document.getElementById('frompostalCode');
	let fromcompanyName = document.getElementById('fromcompanyName');
	let fromphone = document.getElementById('fromphone');
	let fromcountry = document.getElementById('fromcountry');
	let formlength = document.getElementById('formlength');
	let formwidth = document.getElementById('formwidth');
	let formheight = document.getElementById('formheight');
	let formweight = document.getElementById('formweight');
	if (window.serviceId == 1) {
		var signature = document.getElementById('signature').checked;
		var saturday = document.getElementById('saturday').checked;
	} else {
		var signature = '';
		var saturday = '';
	}
	let data = {
		'action': 'createLabel',
		'id': window.serviceId,
		'toaddress1': toaddress1.value,
		'toaddress2': toaddress2.value,
		'toaddress3': toaddress3.value,
		'tocity': tocity.value,
		'tostate': tostate.value,
		'topostalCode': topostalCode.value,
		'tocompanyName': tocompanyName.value,
		'tophone': tophone.value,
		'tocountry': tocountry.value,
		'fromaddress1': fromaddress1.value,
		'fromaddress2': fromaddress2.value,
		'fromaddress3': fromaddress3.value,
		'fromcity': fromcity.value,
		'fromstate': fromstate.value,
		'frompostalCode': frompostalCode.value,
		'fromcompanyName': fromcompanyName.value,
		'fromphone': fromphone.value,
		'fromcountry': fromcountry.value,
		'formlength': formlength.value,
		'formwidth': formwidth.value,
		'formheight': formheight.value,
		'formweight': formweight.value,
		'signature': signature,
		'saturday': saturday,
	};
	res = await sendPost(data);
	if (res['success']) {
		sendMessage('Label Created!')
		location.href = res['url'];
	} else {
		sendMessage(res['msg']);
		return;
	}
	labelBtn.innerHTML = 'Create Label';
	labelBtn.disabled = false;
}

async function setupViewModal(msg, base64) {
	let img = document.getElementById('viewImage');
	img.src = "data:image/png;base64," + base64;
	let title = document.getElementById('viewerModalLabel');
	title.innerHTML = msg;
	if (document.getElementById('printDiv')) {
		document.getElementById('printDiv').remove()
	}
	let body = document.getElementById('viewerBody');
	let print = document.createElement('div');
	// <a class="btn btn-primary" href="#" role="button">Link</a>
	print.innerHTML = `<a onclick="printImg('data:image/png;base64,${base64}')" class="btn btn-primary w-100 mt-2" href="#" role="button">Print</a>`
	print.id = 'printDiv';
	body.appendChild(print);
	const viewerModal = new bootstrap.Modal('#viewerModal', {
		backdrop: true,
		focus: true,
		keyboard: true
	});
	viewerModal.show();
}

function printImg(img) {
  var win = window.open('');
  win.document.write('<img src="' + img + '" onload="window.print();window.close()">');
  win.focus();
}