<script lang="ts">
	
	import { onMount } from 'svelte';

	let coaches = [];
	let teams = []; 

	onMount(async () => {
		const resp = await fetch('http://127.0.0.1:8000/leaderboard', {
			method: 'GET',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
		coaches = data.coach_stats;
		teams = data.team_stats;
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
<style>
	.leaderboard-card {
	  border-radius: 8px;
	  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	  padding: 20px;
	  margin-bottom: 20px;
	  background-color: #fff;
	}
  
	.leaderboard-table {
	  width: 100%;
	  border-collapse: collapse;
	}
  
	.leaderboard-table th,
	.leaderboard-table td {
	  border-bottom: 1px solid #ddd;
	  padding: 8px;
	  text-align: left;
	}
  
	.leaderboard-table th {
	  background-color: #f1f1f1;
	}
  </style>
  
  <div class="leaderboard-card">
	<h1>Leaderboard</h1>
	<table class="leaderboard-table">
	  <thead>
		<tr>
		  <th>Rank</th>
		  <th>Coach</th>
		  <th>Total Equipment Lost</th>
		</tr>
	  </thead>
	  <tbody>
		{#each coaches as coach, index}
		  <tr>
			<td>{index + 1}</td>
			<td>{coach.name}</td>
			<td>{coach.total_equip_lost}</td>
		  </tr>
		{/each}
	  </tbody>
	</table>
  </div>

  <div class="leaderboard-card">
	<h1>Team Leaderboard</h1>
	<table class="leaderboard-table">
	  <thead>
		<tr>
		  <th>Rank</th>
		  <th>Team</th>
		  <th>Total Equipment Lost</th>
		</tr>
	  </thead>
	  <tbody>
		{#each teams as team, index}
		  <tr>
			<td>{index + 1}</td>
			<td>{team.name}</td>
			<td>{team.total_equip_lost}</td>
		  </tr>
		{/each}
	  </tbody>
	</table>
  </div>

  