const downloadButton = document.getElementById("downloadButton");

function downloadFile(data, filename) {
	const json = data;
	const blob = new Blob([json], { type: 'application/json' });
	const url = URL.createObjectURL(blob);
	const a = document.createElement('a');
	a.href = url;
	a.download = filename;
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
}

downloadButton.addEventListener('click', () => {
	const filename = "result.json";
	downloadFile(downloadButton.data, filename);
});
async function uploadCSV() {
	const fileInput = document.getElementById('csvFile');
	const file = fileInput.files[0];
	const statusElement = document.getElementById('status');
	const countAwayElement = document.getElementById('count_away');
	const allPeopleElement = document.getElementById('all_people');
	const predictionType = document.getElementById('predictionType').value;
	const uploadButton = document.querySelector('button');
	const loadingIndicator = document.getElementById('loading');
	const statusElement2 = document.getElementById("count_away");
	const statusElement3 = document.getElementById("all_people");

	statusElement.textContent = '';
	countAwayElement.textContent = '';
	allPeopleElement.textContent = '';

	if (!file) {
		statusElement.textContent = 'Пожалуйста, выберите CSV файл.';
		return;
	}

	if (!file.name.endsWith('.csv')) {
		statusElement.textContent = 'Пожалуйста, выберите валидный CSV файл (с расширением .csv).';
		return;
	}

	try {
		uploadButton.disabled = true;
		loadingIndicator.style.display = 'block';

		const formData = new FormData();
		formData.append('file', file);
		formData.append('prediction_type', predictionType);

		const response = await fetch('http://localhost:8000/process_csv', {
			method: 'POST',
			body: formData,
		});

		if (!response.ok) {
			let errorMessage = `Ошибка при загрузке: ${response.status} ${response.statusText}`;
			try {
				const errorData = await response.json();
				if (errorData.message) {
					errorMessage += ` - ${errorData.message}`;
				}
			} catch (parseError) {
				console.error("Failed to parse error response from server:", parseError);
			}
			throw new Error(errorMessage);
		}

		const data = await response.json();

		statusElement.textContent = data.message || 'Успешно.';
		if (data.type === 'first') {
			statusElement.textContent = "Среднее кол-во решенных задач: " + data.avg;
			statusElement2.textContent = ""
			statusElement3.textContent = ""
			downloadButton.style.display = 'block';
			downloadButton.data = data.file;
		} else {
			statusElement.textContent = "Предпологаемый процент оттока: " + data.avg
			statusElement2.textContent = "Предпологаемое количество оттока: " + data.away_people
			statusElement3.textContent = "Сколько всего людей училось сейчас:" + data.all_people
			downloadButton.style.display = 'block';
			downloadButton.data = data.file;
		}

		fileInput.value = '';

	} catch (error) {
		console.error("Upload error:", error);
		statusElement.textContent = `Ошибка: ${error.message}`;
		downloadButton.style.display = 'none';
	} finally {
		uploadButton.disabled = false;
		loadingIndicator.style.display = 'none';
	}
}