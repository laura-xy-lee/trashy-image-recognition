let model;

const predictButton = document.getElementById('predict');
const fileInput = document.getElementById('file');
const results = document.getElementById("results");

const predict = async () => {

	const files = fileInput.files;

	if (fileInput.value != "") {
		results.innerHTML += `This looks like ... `;
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

const renderResult = (result) => {
	results.innerHTML += `${result.output}`;
	results.innerHTML += `<br/><br/>It looks like it is made of ${result.material_type}`;
	results.innerHTML += `<br/>${result.instruction}`;

}

// Show preview of image when uploaded
var loadFile = function(event) {
	var output = document.getElementById('output');
	output.src = URL.createObjectURL(event.target.files[0]);
};

// When predict button is clicked, run predict function
predictButton.addEventListener("click", () => results.innerHTML = "");
predictButton.addEventListener("click", () => predict());
