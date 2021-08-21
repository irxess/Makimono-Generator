// Script for making the shopping list mode in recipes smoother to use.
// It is possible to wrap every single column item in a row in a label
// and refer to the checkbox by ID, as it is possible to have multiple
// lables per input. But it was horrible to use with all the padding
// and whitespace you simply got no hits on.

const ingredientsTable = document.getElementById("ingredients-table").getElementsByTagName("table")[0];
const shoppingListModeToggle = document.getElementById("toggle-shopping-list-mode");

ingredientsTable.onclick=e=>
{
	if(!shoppingListModeToggle.checked)
	{
		// Don't mark/unmark rows if we're not in the shopping list mode.
		return;
	}
	if (e.target.matches('input[type=checkbox]'))
	{
		// Don't try to toggle the checkbox if the user has just interacted with the checkbox.
		return;
	}
	let row = e.target.closest('tr');
	let ingredientCheckBox = row?.querySelector('input[type=checkbox]');
	if(ingredientCheckBox != undefined)
	{
		ingredientCheckBox.checked = !ingredientCheckBox.checked;
	}
}
