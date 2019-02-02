let model;

const predictButton = document.getElementById('predict');
const fileInput = document.getElementById('file');
const results = document.getElementById("results");

const predict = async () => {

	const files = fileInput.files;

	if (fileInput.value != "") {
		// results.innerHTML += `This looks like ... `;
	} else{
		results.innerHTML += `Please provide an image!`;
	}		

    [...files].map(async (img) => {
        const data = new FormData();
        data.append('file', img);

		const result = await fetch("/predict", 
		{
			method: 'POST',
			body: data
		}).then(response => {
		    return response.json();
		});

		renderResult(result)
	});
}

function vowelTest(s) {
  if (String(s).match('^[aieouAIEOU].*')) {
  	return 'an';
  } else {
  	return 'a';
  }
}

function capitalizeFirstLetter(string) 
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}

const renderResult = (result) => {

	results.innerHTML= ``
	results.innerHTML += `<div class="waste_action">This is ${result.waste_action}!</div>`;
	if (result.instruction != "None") {
		results.innerHTML += `<div class="waste_instruction">${capitalizeFirstLetter(result.instruction)}.`;
	}
	results.innerHTML += `<br/>This looks like ${vowelTest(result.prediction)} ${result.prediction}.`;
	
	if ((result.material != "Unknown") && (result.material != "others")) {
		results.innerHTML += `<br/><br/>Please recycle it as ${capitalizeFirstLetter(result.material)}.`;
	}

	if (result.material != "Unknown") {
		// add link to map
		results.innerHTML += `<br/><br/><form action="https://trashy-demo.herokuapp.com">
			<input type="submit" value="Find your nearest recycling bin" />
			</form>`
	}
}

// Show preview of image when uploaded
var loadFile = function(event) {
	var output = document.getElementById('output');
	output.src = URL.createObjectURL(event.target.files[0]);

	results.innerHTML = ``
};

// When predict button is clicked, run predict function
predictButton.addEventListener("click", () => results.innerHTML = "");
predictButton.addEventListener("click", () => predict());
