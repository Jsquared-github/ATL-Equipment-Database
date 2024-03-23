<script context="module">
	/*export function getUsername(): string {
        // Placeholder function to return the username
        return 'Username';
    }*/
</script>

<script lang="ts">
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import { onMount } from 'svelte';
	onMount(async () => {
		const resp = await fetch('http://127.0.0.1:8000/org', {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	});

	const createAccount = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['username', formData['username']],
			['pwd', formData['password']],
			['category', formData['category']]
		];
		let endpoint = 'http://127.0.0.1:8000/org?';
		for (let param of params) {
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

	const deleteCoach = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['coach', formData['coach']]];
		let endpoint = 'http://127.0.0.1:8000/org/coaches?';
		for (let param of params) {
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
			method: 'DELETE',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
	};
	// import { getUsername } from './+page'; // You don't need to import getUsername here anymore
	// import Item from './item.svelte';
	// import Carousel from './carousel.svelte';

	// Your component script here...
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			Welcome Username to your <br />Equipment Library App
			<!-- Welcome {getUsername()} to your <br />Equipment Library App -->
		</span>
	</h1>

	<div class="checked-out-items">
		<h2>Checked Out Items</h2>
		<!-- Placeholder for checked out items -->
		<!-- <Item /> -->
		<!-- <Item /> -->
	</div>

	<div class="carousel-container">
		<h2>In Stock Items</h2>
		<!-- Placeholder for carousel -->
		<!-- <Carousel /> -->
	</div>

	<div class="checkout-button-container">
		<button>Check out additional items</button>
	</div>

	<div class="login-container">
		<form on:submit={deleteCoach}>
			<div class="input-group">
				<label for="coach">coach:</label>
				<input id="coach" name="coach" type="text" value="" placeholder="Enter your coach" />
			</div>
			<button type="submit">submit</button>
		</form>
	</div>
</section>

<style>
	/* Your existing styles */

	/* Additional styles or modifications */
	.checked-out-items,
	.carousel-container {
		margin: 20px;
	}

	.checkout-button-container {
		display: flex;
		justify-content: center;
		margin-top: 20px;
	}

	button {
		padding: 10px 20px;
		font-size: 18px;
		cursor: pointer;
	}
</style>
