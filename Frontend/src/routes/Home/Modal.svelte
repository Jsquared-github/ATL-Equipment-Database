<script>
    export let show = false;
    export let action = '';
    export let onSubmit;
    export let closeModal;

    let formData = {};

    function handleSubmit(event) {
        event.preventDefault();
        onSubmit(formData, action);
    }

    function handleChange(event) {
        formData[event.target.name] = event.target.value;
    }
</script>

{#if show}
<div class="modal">
    <form on:submit={handleSubmit}>
        {#if action === 'createUser'}
        <input type="text" name="username" on:change={handleChange} placeholder="Username">
        <input type="password" name="password" on:change={handleChange} placeholder="Password">
        <select name="category" on:change={handleChange}>
            <option value="standard">Standard</option>
            <option value="admin">Admin</option>
        </select>
        {/if}
        <!-- Add other actions as needed -->
        <button type="submit">Submit</button>
        <button type="button" on:click={closeModal}>Cancel</button>
    </form>
</div>
{/if}

<style>
    .modal {
        position: fixed;
        left: 0;
        top: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .modal form {
        background: white;
        padding: 20px;
        border-radius: 8px;
    }
</style>
