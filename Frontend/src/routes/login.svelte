<script lang="ts">
	import { goto } from '$app/navigation';
	let username: string;
	let password: string;

	function routeToPage(route: string, replaceState: boolean) {
		goto(`/${route}`, { replaceState });
	}
	const handleLogin = async () => {
		console.log('Working');
		let form = new FormData();
		form.append('username', username);
		form.append('password', password);
		const resp = await fetch('http://127.0.0.1:8000/login', {
			method: 'POST',
			body: form
		});
		const user = await resp.json();
		console.log(user.access_token);
		localStorage.setItem('token', user.access_token);
		routeToPage('home', false);
	};
</script>

<div class="login-container">
	<form on:submit|preventDefault={handleLogin}>
		<div class="input-group">
			<label for="Username">Email:</label>
			<input id="username" type="text" bind:value={username} placeholder="Enter your username" />
		</div>
		<div class="input-group">
			<label for="password">Password:</label>
			<input
				id="password"
				type="password"
				bind:value={password}
				placeholder="Enter your password"
			/>
		</div>
		<button type="submit">Login</button>
	</form>
</div>

<style>
	.login-container {
		/* Style your login container */
	}

	.input-group {
		margin-bottom: 1rem;
	}

	label {
		display: block;
		margin-bottom: 0.5rem;
	}

	input {
		width: 100%;
		padding: 0.5rem;
		font-size: 1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
	}

	button {
		/* Style your button */
	}

	/* Additional styling */
</style>
