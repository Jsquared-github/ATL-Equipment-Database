<script lang="ts">
	import { onMount } from 'svelte';
	onMount(async () => {
		const resp = await fetch('http://127.0.0.1:8000/library', {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	});

	const checkoutEquipment = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['coach', formData['coach']],
			['team', formData['team']],
			['quantity', formData['quantity']]
		];
		let endpoint = `http://127.0.0.1:8000/library/${formData['equip']}?`;
		console.log(params);
		for (let param of params) {
			param[1] = param[1].replaceAll(' ', '+');
			if (param[1] == '') {
				console.log('Fill in all fields');
				return;
			}
			if (endpoint.slice(-1) !== '?') {
				endpoint += `&${param[0]}=${param[1]}`;
			} else {
				endpoint += `${param[0]}=${param[1]}`;
			}
		}
		const resp = await fetch(endpoint, {
			method: 'POST',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	};

	const checkinEquipment = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['coach', formData['coach']],
			['team', formData['team']],
			['quantity', formData['quantity']]
		];
		let endpoint = `http://127.0.0.1:8000/library/${formData['equip']}?`;
		console.log(params);
		for (let param of params) {
			param[1] = param[1].replaceAll(' ', '+');
			if (param[1] == '') {
				console.log('Fill in all fields');
				return;
			}
			if (endpoint.slice(-1) !== '?') {
				endpoint += `&${param[0]}=${param[1]}`;
			} else {
				endpoint += `${param[0]}=${param[1]}`;
			}
		}
		const resp = await fetch(endpoint, {
			method: 'PUT',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	};
</script>

<div class="login-container">
	<form on:submit={checkinEquipment}>
		<div class="input-group">
			<label for="coach">coach:</label>
			<input id="coach" name="coach" type="text" value="" placeholder="Enter your coach" />
		</div>
		<div class="input-group">
			<label for="team">team:</label>
			<input id="team" name="team" type="text" value="" placeholder="Enter your team" />
		</div>
		<div class="input-group">
			<label for="equip">equipment:</label>
			<input id="equip" name="equip" type="text" value="" placeholder="Enter your equipment" />
		</div>
		<div class="input-group">
			<label for="quantity">quantity:</label>
			<input id="quantity" name="quantity" type="text" value="" placeholder="Enter your quantity" />
		</div>
		<button type="submit">submit</button>
	</form>
</div>
