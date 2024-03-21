<script lang="ts">
  import { goto } from '$app/navigation';
    let email = '';
    let password = '';

    function routeToPage(route: string, replaceState: boolean) {
     goto(`/${route}`, { replaceState })  
    }
    const handleLogin = async () => {
      console.log('Working')
      routeToPage('Home', false)
      // Here you would implement your login logic, like calling an API.
    };
  </script>
  
  <div class="login-container">
    <form on:submit|preventDefault={handleLogin}>
      <div class="input-group">
        <label for="email">Email:</label>
        <input id="email" type="email" bind:value={email} placeholder="Enter your email" />
      </div>
      <div class="input-group">
        <label for="password">Password:</label>
        <input id="password" type="password" bind:value={password} placeholder="Enter your password" />
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
  