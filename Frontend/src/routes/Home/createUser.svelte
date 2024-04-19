<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    export let show = false;
    export let submitUser;

    const dispatch = createEventDispatcher();

    let username = '';
    let password = '';
    let category = '';

    function handleSubmit() {
        submitUser({ username, password, category });
        username = '';
        password = '';
        category = '';
        close();
    }

    function close() {
        dispatch('close');
    }
</script>

{#if show}
<div class="modal">
    <div class="modal-content">
        <span class="close" on:click={close}>&times;</span>
        <form on:submit|preventDefault={handleSubmit}>
            <label>Username:
                <input type="text" bind:value={username} required>
            </label>
            <label>Password:
                <input type="password" bind:value={password} required>
            </label>
            <label>Category:
                <select bind:value={category} required>
                    <option value="" disabled selected>Select your category</option>
                    <option value="admin">Admin</option>
                    <option value="coach">Coach</option>
                    <option value="player">Player</option>
                </select>
            </label>
            <button type="submit">Create User</button>
        </form>
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
