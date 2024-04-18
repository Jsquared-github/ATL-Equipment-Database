<script lang="ts">
	import { onMount } from 'svelte';

let data = {
  total_equip_lost: 0,
  total_cost: 0,
  avg_daily_equip_loss: 0,
  avg_daily_cost: 0,
  top_equips_lost: {}
};

onMount(async () => {
  const resp = await fetch('http://127.0.0.1:8000/dashboard', {
	method: 'GET',
	headers: { Authorization: `Bearer ${localStorage.token}` }
  });
  data = await resp.json();
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
<style>
	.dashboard {
	  display: grid;
	  grid-template-columns: repeat(3, 1fr);
	  gap: 16px;
	  margin: 16px;
	}
	
	.card {
	  background: #fff;
	  border-radius: 8px;
	  padding: 20px;
	  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
	}
  
	.card-header {
	  font-size: 1.5rem;
	  margin-bottom: 16px;
	}
  
	.card-content {
	  font-size: 1rem;
	}
  
	.card.highlight {
	  border: 2px solid blue; /* Highlight style */
	}
  </style>
  
  <div class="dashboard">
	<div class="card highlight">
	  <div class="card-header">Total Items Lost</div>
	  <div class="card-content">{data.total_equip_lost}</div>
	</div>
  
	<div class="card">
	  <div class="card-header">Total Cost ($)</div>
	  <div class="card-content">{data.total_cost}</div>
	</div>
  
	<div class="card">
	  <div class="card-header">AVG Daily Items Lost</div>
	  <div class="card-content">{data.avg_daily_equip_loss}</div>
	</div>
  
	<div class="card">
	  <div class="card-header">AVG Daily Cost ($)</div>
	  <div class="card-content">{data.avg_daily_cost}</div>
	</div>
  
	<div class="card">
	  <div class="card-header">Top 5 Equipment Lost</div>
	  <div class="card-content">
		<ul>
		  {#each Object.entries(data.top_equips_lost) as [equip, count]}
			<li>{equip}: {count}</li>
		  {/each}
		</ul>
	  </div>
	</div>
  </div>
