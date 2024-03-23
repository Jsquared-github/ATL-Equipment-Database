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
</script>
