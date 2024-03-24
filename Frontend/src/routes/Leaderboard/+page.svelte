<script lang="ts">
	import { onMount } from 'svelte';
	onMount(async () => {
		const resp = await fetch('http://127.0.0.1:8000/leaderboard', {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	});
	const updateLeaderboard = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['metric', formData['metric']],
			['period', formData['period']]
		];
		let endpoint = 'http://127.0.0.1:8000/leaderboard?';
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
