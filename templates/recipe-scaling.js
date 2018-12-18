function resetScaling(){
	document.getElementById('percent-number').value = 100;
	document.getElementById('percent-slider').value = 100;
	var amountElements = document.getElementsByClassName('amount');
	for (var i = 0; i < amountElements.length; i++) {
		amountElements[i].textContent = amountElements[i].getAttribute('data-original-amount');
	}
}

function scaleByPercentNumber(){
	var percentValue = document.getElementById('percent-number').value;
	if(percentValue > 0){
		document.getElementById('percent-slider').value = percentValue;
		applyScaling(percentValue/100);
	}
	else {
		resetScaling();
	}
}


function scaleByPercentSlider(){
	var currentSliderValue = document.getElementById('percent-slider').value;
	document.getElementById('percent-number').value = currentSliderValue;
	applyScaling(currentSliderValue/100);
}

function scaleByIngredient(){
}

function applyScaling(percentageToScaleBy) {
	var amountElements = document.getElementsByClassName('amount');
	for (var i = 0; i < amountElements.length; i++) {
		var calculatedValue = percentageToScaleBy * amountElements[i].getAttribute('data-original-amount');
		var roundedResult = roundNumber(calculatedValue, 2);
		amountElements[i].textContent = roundedResult;
	}
}

function roundNumber(number, decimalPlaces) {
	return +(Math.round(number + "e+" + decimalPlaces)  + "e-" + decimalPlaces);
}
