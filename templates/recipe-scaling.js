function resetScaling(){
	document.getElementById('percent-number').value = 100;
	document.getElementById('percent-slider').value = 100;
	document.getElementById('ingredient-inputted-amount').value = "";
	var amountElements = document.getElementsByClassName('amount');
	for (var i = 0; i < amountElements.length; i++) {
		amountElements[i].textContent = amountElements[i].getAttribute('data-original-amount');
	}
}

function scaleByPercentNumber(){
	var percentValue = document.getElementById('percent-number').value;
	if(percentValue >= 0){
		var slider = document.getElementById('percent-slider');
		if(slider.value != percentValue){
			slider.value = percentValue;
		}
		applyScaling(percentValue/100);
	}
}


function scaleByPercentSlider(){
	var currentSliderValue = document.getElementById('percent-slider').value;
	var percentField = document.getElementById('percent-number');
	if(percentField.value != currentSliderValue){
		percentField.value = currentSliderValue;
	}
	applyScaling(currentSliderValue/100);
}

function scaleByIngredient(){
	var ingredientsMenu = document.getElementById('ingredient-select');
	var selectedIngredientOriginalAmount = ingredientsMenu.options[ingredientsMenu.selectedIndex].value;
	var userDesiredAmount = document.getElementById('ingredient-inputted-amount').value;
	var percentageToScaleBy = userDesiredAmount/selectedIngredientOriginalAmount;
	applyScaling(percentageToScaleBy);
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
