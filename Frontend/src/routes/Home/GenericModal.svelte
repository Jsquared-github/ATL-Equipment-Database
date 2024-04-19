<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    export let show = false;
    export let content;
    export let onSubmit;
    export let onClose;

    const dispatch = createEventDispatcher();

    function handleSubmit(event) {
        event.preventDefault();
        onSubmit(); // Call the onSubmit function passed as a prop
        close(); // Close modal after form submission
    }

    function close() {
        dispatch('close'); // Notify the parent component to close the modal
        if (onClose) onClose(); // Optional additional onClose behavior
    }
</script>

{#if show}
<div class="modal">
    <div class="modal-content">
        <span class="close" on:click={close}>&times;</span>
            <slot></slot> <!-- Use slots to allow custom form content -->
    </div>
</div>
{/if}

<style>
    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
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
        font-size: 24px;
        cursor: pointer;
    }
</style>

