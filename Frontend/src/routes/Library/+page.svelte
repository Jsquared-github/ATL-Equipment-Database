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
