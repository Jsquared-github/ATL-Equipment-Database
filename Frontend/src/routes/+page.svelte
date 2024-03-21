<script>
	import Login from './login.svelte';
	
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
  </script>
  
  <svelte:head>
	  <title>Home</title>
	  <meta name="description" content="Svelte demo app" />
  </svelte:head>
  
  <section>
	  <h1>
		  <span class="welcome">
			  
		  </span>
		  Welcome to your <br />Equipment Library App
	  </h1>
  
	  <Login /> <!-- Login component inserted here -->
  
  </section>
  
  <style>
	  /* ... your existing styles ... */
  
	  /* Additional styles or modifications can go here */
  </style>
  