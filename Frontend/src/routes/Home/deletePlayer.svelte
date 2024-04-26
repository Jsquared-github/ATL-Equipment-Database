<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    //import { orgData } from './store';
    export let playerData;
    export let show = false;
    const dispatch = createEventDispatcher();
    let selectedPlayerId = '';
    import { onMount } from 'svelte';
    import { orgData } from './store';
    let players = [];

    onMount(async () => {
		try {
			const response = await fetch('http://127.0.0.1:8000/org', {
				method: 'GET',
				headers: { Authorization: `Bearer ${localStorage.token}` }
			});

			if (response.ok) {
				const data = await response.json();
				console.log(data);

                
                
                for (const [key, value] of Object.entries(data.players)) {
                    players.push({
                        ...value,
                        playerID: key
                    });
                }
                console.log(players);

				orgData.set({
					teams: data.teams || [],
					coaches: data.coaches || [],
					players: players || [],
					equipment: data.equipment || []
				});
			} else {
				throw new Error('Network response was not ok.');
			}
		} catch (error) {
			console.error('There has been a problem with your fetch operation:', error);
		}
	});
    console.log($orgData);


    // $: if ($orgData.coaches && $orgData.coaches.length > 0) {
    //     console.log('Coaches available:', $orgData.coaches);
    // } else if (show) {
    //     console.log('No coaches available');
    // }
 
    async function deletePlayer() {
        if (!selectedPlayerId) {
            alert('Please select a coach to delete.');
            return;
        }
        try {
            const response = await fetch(`http://127.0.0.1:8000/org/players?player=${selectedPlayerId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${localStorage.token}`,
                    'Content-Type': 'application/json'
                }
            });
            const result = await response.text();  // This will capture the response text, which might be empty for a DELETE request
            console.log('Server response:', result);

            if (!response.ok) {
                throw new Error(result || 'Failed to delete player');
            }

            // orgData.update(data => {
            //     const index = data.coaches.findIndex(c => c.coachID === selectedCoachId);
            //     if (index !== -1) data.coaches.splice(index, 1);
            //     return data;
            // });
            close();
        } catch (error) {
            console.error('Error:', error);
            alert(`Error deleting team: ${error.message}`);
        }
    }

    function close() {
        dispatch('close');
        selectedPlayerId = '';
    }
</script>
{#if show}
<div class="modal">
    <div class="modal-content">
        <span class="close" on:click={close}>&times;</span>
        <h2>Delete Player</h2>
        {#if players && players.length > 0}
            <select bind:value={selectedPlayerId}>
                <option value="" disabled selected>Select a player to delete</option>
                {#each players as player}
                    <option value={player.playerID}>{player.playerID}</option>
                {/each}
            </select>
            <button on:click={deletePlayer}>Delete Player</button>
        {:else}
            <p>No players available to delete .</p>
        {/if}
    </div>
</div>
{/if}
<style>
    .modal {
        position: fixed;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 5px;
        position: relative;
    }
    .close {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        font-size: 24px;
    }
</style>
