window.addEventListener('load', function() {
	// Because the ingredient values reset at load to the default values embedded in the html the scaling should reflect that as well.
	// Do not call the resetScaling() function here,
	// because all the amounts are already set to their default value,
	// and there is no need to traverse the entire document to update them to the value they already have.
	adjustAllScalingFieldsToMatchPercentageScale(1);
});

function resetScaling(){
	adjustAllScalingFieldsToMatchPercentageScale(1);

	// Use the embedded original amout data rather than the scale calculation function with input "1".
	// One reason is that it avvoids wasting time with uneccessary calculations.
	// Another is that it makes the reset function less prone to bugs in the calculation function (which is one reason why you might want to reset).
	var amountElements = document.getElementsByClassName('amount');
	for (var i = 0; i < amountElements.length; i++) {
		amountElements[i].textContent = amountElements[i].getAttribute('data-original-amount');
	}
}

function scaleByPercentNumber(){
	var displayPercentValue = document.getElementById('percent-number').value;
	if(displayPercentValue >= 0){
		var percentageToScaleBy = displayPercentValue/100;
		updateScaling(percentageToScaleBy);
	}
}

function scaleByPercentSlider(){
	var currentSliderValue = document.getElementById('percent-slider').value;
	var percentageToScaleBy = currentSliderValue/100;
	updateScaling(percentageToScaleBy);
}

function scaleByIngredient(){
	var ingredientsMenu = document.getElementById('ingredient-select');
	var selectedIngredientOriginalAmount = ingredientsMenu.options[ingredientsMenu.selectedIndex].value;
	var userDesiredAmount = document.getElementById('ingredient-inputted-amount').value;
	var percentageToScaleBy = userDesiredAmount/selectedIngredientOriginalAmount;
	updateScaling(percentageToScaleBy);
}

function updateScaling(percentageToScaleBy){
	adjustAllScalingFieldsToMatchPercentageScale(percentageToScaleBy);
	applyScalingToIngredients(percentageToScaleBy);
}

function applyScalingToIngredients(percentageToScaleBy) {
	var amountElements = document.getElementsByClassName('amount');
	for (var i = 0; i < amountElements.length; i++) {
		var calculatedValue = percentageToScaleBy * amountElements[i].getAttribute('data-original-amount');
		var roundedResult = roundNumber(calculatedValue, 2);
		amountElements[i].textContent = roundedResult;
	}
}

// Round numbers so that they are pretty for displaying, following these rules:
//  - Cut trailing zeroes behind decimal point (or the entire decimal point if there are only trailing zeroes).
//  - Round the number to the chosen amount of decimal places.
//  - Allow the number be of arbitrary length befor the decimals.
function roundNumber(number, decimalPlaces) {
	return +(Math.round(number + "e+" + decimalPlaces)  + "e-" + decimalPlaces);
}

function adjustAllScalingFieldsToMatchPercentageScale(percentageToScaleBy){
	adjustScaleByPercentNumberToMatchPercentageScale(percentageToScaleBy);
	adjustScaleByPercentSliderToMatchPercentageScale(percentageToScaleBy);
	adjustScaleByIngredientToMatchPercentageScale(percentageToScaleBy);
}

function adjustScaleByPercentNumberToMatchPercentageScale(percentageToScaleBy){
	var percentField = document.getElementById('percent-number');
	var displayPercentage = percentageToScaleBy * 100;
	// When scaling by ingredient you could end up seeing some really funky values.
	// While it is fun to teach people about the joy of floating point arithmetic, it just not very pretty.
	// Therefore, rount it to 2 decimal places.
	var roundedDisplayPercentage = roundNumber(displayPercentage, 2);
	if(percentField.value != roundedDisplayPercentage){
		percentField.value = roundedDisplayPercentage;
	}
}

// It's not like the slider meaningfully represents values beyond the range set so that it is somewhat usable
// (infinite resolution and/or range would be pretty unusable for a selector in the shape of a line wiht a fixed length).
// So just set it to whatever percentage value that is supplied,
// if its outside the range it will just be at it's max,
// and it's not really possible to notice the difference in position for the "uselectable" values in practice.
function adjustScaleByPercentSliderToMatchPercentageScale(percentageToScaleBy){
	var slider = document.getElementById('percent-slider');
	var displayPercentage = percentageToScaleBy * 100;
	if(slider.value != displayPercentage){
		slider.value = displayPercentage;
	}
}

function adjustScaleByIngredientToMatchPercentageScale(percentageToScaleBy){
	var ingredientsMenu = document.getElementById('ingredient-select');
	var selectedIngredientOriginalAmount = ingredientsMenu.options[ingredientsMenu.selectedIndex].value;
	var scaledValue = percentageToScaleBy * selectedIngredientOriginalAmount;
	// Round the result to the same precision as when applying scaling so that the displayed numbers look more equal:
	var roundedResult = roundNumber(scaledValue, 2);
	var ingredientScalingAmountInputElement = document.getElementById('ingredient-inputted-amount');
	if(ingredientScalingAmountInputElement.value != roundedResult){
		ingredientScalingAmountInputElement.value = roundedResult;
	}
}
