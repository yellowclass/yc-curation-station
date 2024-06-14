const sendPostRequest = async (url = '', data = {}) => {
	// Default options are marked with *
	const response = await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
			// 'Authorization': 'Bearer your-token-here' // Include this if you need to send an auth token
		},
		body: JSON.stringify(data) // body data type must match "Content-Type" header
	});

	// Check if the response status is OK (status code 200-299)
	if (!response.ok) {
		throw new Error('Network response was not ok ' + response.statusText);
	}

	// Parse the JSON from the response
	return response.json(); // parses JSON response into native JavaScript objects
};

function displayChat(chatData) {
	const chatContainer = document.getElementById('chat-container');

	chatData.forEach(chat => {
		// Create a container for the user's message
		const userMessage = document.createElement('div');
		userMessage.classList.add('chat-message', 'user');

		const userMessageDiv = document.createElement('div');
		userMessageDiv.classList.add('message-content', 'user-message');
		userMessageDiv.textContent = chat.message;

		userMessage.appendChild(userMessageDiv);
		chatContainer.appendChild(userMessage);

		// Create a container for GPT's reply
		const gptMessage = document.createElement('div');
		gptMessage.classList.add('chat-message', 'gpt');

		const gptReplyDiv = document.createElement('div');
		gptReplyDiv.classList.add('message-content', 'gpt-reply');
		gptReplyDiv.textContent = chat.gptReply;

		gptMessage.appendChild(gptReplyDiv);
		chatContainer.appendChild(gptMessage);
	});

	// Ensure the container is always scrolled to the bottom when new content is added

	chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sendMessage() {
	const input = document.getElementById('messageInput');
	const button = document.getElementById('sendButton');
	const message = input.value;

	if (message.trim() === '') {
		return;
	}

	button.disabled = true;

	fetch('/api/curationStation/send-message', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			message: message,
			userId: Number(getQueryParam('userId')),
			botId: Number(getQueryParam('botId'))
		})
	})
		.then(response => {
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			return response.json();
		})
		.then(data => {
			console.log('Success:', data);
			input.value = '';
			location.reload();
		})
		.catch(error => {
			console.error('Error:', error);
		})
		.finally(() => {
			button.disabled = false;
		});
}

function getQueryParam(name) {
	const urlParams = new URLSearchParams(window.location.search);
	return urlParams.get(name);
}

function handleKeyPress(event) {
	if (event.key === 'Enter') {
		sendMessage();
	}
}

// Function to generate the profile card HTML
function generateProfileCard(profileData) {
	const profileCard = document.getElementById('profileCard');

	// Creating elements
	const cardContainer = document.createElement('div');
	const nameElement = document.createElement('h2');
	const designationElement = document.createElement('p');
	const professionElement = document.createElement('p');
	const personalLifeElement = document.createElement('p');
	const interestsElement = document.createElement('p');
	const availabilityElement = document.createElement('p');

	// Setting content
	nameElement.textContent = profileData.name;
	designationElement.textContent = profileData.designation;
	professionElement.textContent = profileData.profession;
	personalLifeElement.textContent = profileData.personalLife;
	interestsElement.textContent = profileData.Interests;
	availabilityElement.textContent = profileData.Availability;

	// Appending elements
	cardContainer.appendChild(nameElement);
	cardContainer.appendChild(designationElement);
	cardContainer.appendChild(professionElement);
	cardContainer.appendChild(personalLifeElement);
	cardContainer.appendChild(interestsElement);
	cardContainer.appendChild(availabilityElement);

	// Adding styles
	cardContainer.classList.add('profile-card');

	// Appending the card to the container
	profileCard.appendChild(cardContainer);
}

(async () => {
	let botData = (
		await sendPostRequest('/api/curationStation/get-bot-info', {
			botId: Number(getQueryParam('botId'))
		})
	).data;
	console.log(botData);
	generateProfileCard(JSON.parse(botData));

	let chatData = (
		await sendPostRequest('/api/curationStation/get-full-chat', {
			userId: Number(getQueryParam('userId')),
			botId: Number(getQueryParam('botId'))
		})
	).data;
	chatData = JSON.parse(chatData);

	console.log(chatData);

	displayChat(chatData);
})();
