<script lang="ts">
	 import { onMount } from 'svelte';
    import { orgData } from './store'; // Assuming the store is correctly imported from a central location

    // Fetch and update orgData on component mount
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

	// const checkoutEquipment = async (e: HTMLFormElement) => {
	// 	const form = new FormData(e.target);
	// 	console.log(form);
	// 	const formData = {};
	// 	for (let field of form) {
	// 		const [key, value] = field;
	// 		formData[key] = value;
	// 	}
	// 	let params = [
	// 		['coach', formData['coach']],
	// 		['team', formData['team']],
	// 		['quantity', formData['quantity']]
	// 	];
	// 	let endpoint = `http://127.0.0.1:8000/library/${formData['equip']}?`;
	// 	console.log(params);
	// 	for (let param of params) {
	// 		param[1] = param[1].replaceAll(' ', '+');
	// 		if (param[1] == '') {
	// 			console.log('Fill in all fields');
	// 			return;
	// 		}
	// 		if (endpoint.slice(-1) !== '?') {
	// 			endpoint += `&${param[0]}=${param[1]}`;
	// 		} else {
	// 			endpoint += `${param[0]}=${param[1]}`;
	// 		}
	// 	}
	// 	const resp = await fetch(endpoint, {
	// 		method: 'POST',
	// 		headers: { Authorization: `Bearer ${localStorage.token}` }
	// 	});
	// 	const data = await resp.json();
	// 	console.log(data);
	// };

	const checkoutEquipment = async (e: any ) =>{
		let endpoint = `http://127.0.0.1:8000/library/${e.equipName}?coach=coach1&team=team1&quantity=1`;
		console.log(e);
		const resp = await fetch(endpoint, {
			method: 'POST',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
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
	}

	const checkinEquipment = async (e: any ) =>{
		let endpoint = `http://127.0.0.1:8000/library/${e.equipName}?coach=coach1&team=team1&quantity=1`;
		console.log(e);
		const resp = await fetch(endpoint, {
			method: 'PUT',
			headers: { Authorization: `Bearer ${localStorage.token}` }
		});
		const data = await resp.json();
		console.log(data);
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
	}

// 	const checkinEquipment = async (e: HTMLFormElement) => {
//     const form = new FormData(e.target);
//     const formData = {};
//     for (let field of form) {
//         const [key, value] = field;
//         formData[key] = value;
//     }
//     let params = [
//         ['coach', formData['coach']],
//         ['team', formData['team']],
//         ['quantity', formData['quantity']]
//     ];
//     let endpoint = `http://127.0.0.1:8000/library/${formData['equip']}?`;
//     console.log(params);
//     for (let param of params) {
//         param[1] = param[1].replace(/ /g, '+'); // Use regular expression for global replacement
//         if (param[1] == '') {
//             console.log('Fill in all fields');
//             return;
//         }
//         if (endpoint.slice(-1) !== '?') {
//             endpoint += `&${param[0]}=${param[1]}`;
//         } else {
//             endpoint += `${param[0]}=${param[1]}`;
//         }
//     }
//     const resp = await fetch(endpoint, {
//         method: 'PUT',
//         headers: { Authorization: `Bearer ${localStorage.token}` }
//     });
//     const data = await resp.json();
//     console.log(data);
// };
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
		<div class="card-header">Equipment</div>
		<div class="card-content">
			{#each Object.values($orgData.equipment || {}) as equipment}
				<div class="item">
					{equipment.equipmentID} - {equipment.equipName} ({equipment.currQuantity})
					<button on:click={() => checkoutEquipment(equipment)}>Checkout</button>
					<button on:click={() => checkinEquipment(equipment)}>Checkin</button>
				</div>
			{/each}
		</div>
	</div>
	

    <!-- Action Panel Added Below -->
    
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

    .action-panel {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        padding: 1rem;
        margin-top: 1rem; /* Additional space above the panel */
    }

    .action-panel button {
        margin: 5px;
        padding: 0.6rem 1rem;
        border: none;
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        cursor: pointer;
    }

    .action-panel button:hover {
        background-color: #0056b3;
    }
</style>