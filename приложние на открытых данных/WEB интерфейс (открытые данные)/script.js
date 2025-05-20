async function submitForm(event) {
	event.preventDefault(); // Предотвращение стандартной отправки формы

	const formData = new FormData(event.target);
	const formDataObj = {};

	formData.forEach((value, key) => {
		formDataObj[key] = value;
	});

	try {
		const response = await fetch('http://127.0.0.1:8000/process_form', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(formDataObj)
		});

		if (response.ok) {
			const result = await response.json();
			console.log('Успешно:', result);
			document.getElementById('probabilityResult').innerText = 'Вероятность: ' + result.probability;

		} else {
			console.error('Ошибка:', response.status);
			alert('Ошибка при отправке данных.  Пожалуйста, проверьте консоль.');
		}
	} catch (error) {
		console.error('Ошибка:', error);
		alert('Произошла ошибка при отправке данных. Пожалуйста, проверьте консоль.');
	}
}

function selectCourse(element) {
	// 1. Удалить класс "selected" у всех картинок
	const images = document.querySelectorAll('.course-image');
	images.forEach(img => img.classList.remove('selected'));

	// 2. Добавить класс "selected" к выбранной картинке
	element.classList.add('selected');

	// 3. Обновить значение скрытого поля
	const selectedCourse = element.dataset.course;
	document.getElementById('selected_course').value = selectedCourse;
}
function selectDevice(element) {
	// Сбросить выбор всех устройств
	document.querySelectorAll('.device-image').forEach(img => img.classList.remove('selected'));

	// Выбрать текущее устройство
	element.classList.add('selected');

	// Обновить скрытое поле
	document.getElementById('selected_device').value = element.dataset.device;
}
function updateValue(elementId, value) {
	document.getElementById(elementId + '_value').innerText = value;
}