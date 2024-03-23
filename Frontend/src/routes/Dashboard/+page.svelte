<script lang="ts">
	import { onMount } from 'svelte';
	onMount(async () => {
		const resp = await fetch('http://127.0.0.1:8000/dashboard', {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	});
	const updateDashboard = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['coach', formData['coach']],
			['team', formData['team']],
			['period', formData['period']]
		];
		let endpoint = 'http://127.0.0.1:8000/dashboard?';
		for (let param of params) {
			if (param[1] !== '') {
				if (endpoint.slice(-1) !== '?') {
					endpoint += `&${param[0]}=${param[1]}`;
				} else {
					endpoint += `${param[0]}=${param[1]}`;
				}
			}
		}
		const resp = await fetch(endpoint, {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	};
</script>

<div class="login-container">
	<form on:submit={updateDashboard}>
		<div class="input-group">
			<label for="coach">coach:</label>
			<input id="coach" name="coach" value="" type="text" placeholder="Enter your coach" />
		</div>
		<div class="input-group">
			<label for="team">team:</label>
			<input id="team" name="team" type="text" value="" placeholder="Enter your team" />
		</div>
		<div class="input-group">
			<label for="period">period:</label>
			<input id="period" name="period" value="" type="text" placeholder="Enter your period" />
		</div>
		<button type="submit">submit</button>
	</form>
</div>
