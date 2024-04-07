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
    import { writable } from 'svelte/store';
    import { orgData } from './store';

    // Initialize with empty arrays
    onMount(async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/org', {
                method: 'GET',
                headers: { Authorization: `Bearer ${localStorage.token}` }
            });

            if (response.ok) {
                const data = await response.json();
                console.log(data);

                orgData.set({
                    teams: data.teams || [],
                    coaches: data.coaches || [],
                    players: data.players || [],
                    equipment: data.equipment || []
                });
            } else {
                throw new Error('Network response was not ok.');
            }
        } catch (error) {
            console.error('There has been a problem with your fetch operation:', error);
        }
    });

    orgData.subscribe(value => {
        if (value.coaches.length > 0) {
            console.log(value.coaches[0]); // Log the first coach object
        }
    });

	const createUser = async (e: HTMLFormElement) => {
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

	const deletePlayer = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['player', formData['player']]];
		let endpoint = 'http://127.0.0.1:8000/org/players?';
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

	const assignCoach = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = `http://127.0.0.1:8000/org/coaches/${formData['coach']}?`;
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

	const assignPlayer = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = `http://127.0.0.1:8000/org/players/${formData['player']}?`;
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

	const unassignCoach = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = `http://127.0.0.1:8000/org/coaches/${formData['coach']}?`;
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

	const unassignPlayer = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = `http://127.0.0.1:8000/org/players/${formData['player']}?`;
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

	const createTeam = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = 'http://127.0.0.1:8000/org/teams?';
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

	const deleteTeam = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['team', formData['team']]];
		let endpoint = 'http://127.0.0.1:8000/org/teams?';
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

	const createEquipment = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [
			['equip', formData['equip']],
			['unitPrice', formData['unitPrice']],
			['quantity', formData['quantity']]
		];
		let endpoint = 'http://127.0.0.1:8000/org/equipment?';
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

	const deleteEquipment = async (e: HTMLFormElement) => {
		const form = new FormData(e.target);
		const formData = {};
		for (let field of form) {
			const [key, value] = field;
			formData[key] = value;
		}
		let params = [['equip', formData['equip']]];
		let endpoint = 'http://127.0.0.1:8000/org/equipment?';
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

<div class="home-layout">
    <h1>
        <span class="welcome">
            Welcome Username to your <br />Equipment Library App
        </span>
    </h1>
  
    <div class="category-card">
        <div class="card-header">Coaches</div>
        <div class="card-content">
            {#each Object.values($orgData.coaches || {}) as coach}
                <div class="item">{coach.coachID} - {coach.tID}</div>
            {/each}
        </div>
    </div>
  
    <div class="category-card">
        <div class="card-header">Teams</div>
        <div class="card-content">
            {#each Object.values($orgData.teams || {}) as team}
                <div class="item">{team.teamID} - {team.teamName}</div>
            {/each}
        </div>
    </div>
  
    <div class="category-card">
        <div class="card-header">Equipment</div>
        <div class="card-content">
            {#each Object.values($orgData.equipment || {}) as equipment}
                <div class="item">{equipment.equipmentID} - {equipment.equipName} ({equipment.currQuantity})</div>
            {/each}
        </div>
    </div>
</div>

<style>
    .home-layout {
        /* Adjust layout styles as needed */
    }

    .category-card {
        margin: 1rem;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .card-header {
        padding: 0.5rem;
        background-color: #f0f0f0;
        border-bottom: 1px solid #ddd;
        text-align: center;
    }

    .card-content {
        height: 150px; /* Adjust height as needed */
        overflow-y: auto;
        padding: 0.5rem;
    }

    .item {
        padding: 0.25rem;
        border-bottom: 1px solid #eee;
    }
</style>
