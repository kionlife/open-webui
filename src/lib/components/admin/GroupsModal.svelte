<script lang="ts">
	import { getContext } from 'svelte';
	import Modal from '../common/Modal.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import { getGroups, addGroup, updateGroup, destroyGroup } from '$lib/apis/groups';
	import { onMount } from 'svelte';

	const i18n = getContext('i18n');

	export let show = false;
	let groups = [];
	let newGroupName = '';
	let editedGroupName = '';
	let selectedGroupId = 0;
	let addGroupInput = false;
	let token = localStorage.token;

	onMount(async () => {
		await fetchGroups();
	});

	async function fetchGroups() {
		try {
			const fetchedGroups = await getGroups(token);
			groups = fetchedGroups;
		} catch (error) {
			console.error(error);
		}
	}

	async function createGroup() {
		if (newGroupName.trim()) {
			try {
				const newGroup = await addGroup(token, newGroupName);
				groups = [...groups, newGroup];
				newGroupName = '';
			} catch (error) {
				console.error(error);
			}
		}
	}

	function selectGroup(id: number) {
		selectedGroupId = id;
		const group = groups.find(g => g.id === id);
		if (group) {
			editedGroupName = group.name;
		}
	}

	async function editGroup() {
		if (editedGroupName.trim() && selectedGroupId !== 0) {
			try {
				const updatedGroup = await updateGroup(token, selectedGroupId, editedGroupName);
				groups = groups.map(group =>
					group.id === selectedGroupId ? updatedGroup : group
				);
				editedGroupName = '';
				selectedGroupId = 0;
			} catch (error) {
				console.error(error);
			}
		}
	}

	async function deleteGroup(id: number) {
		try {
			await destroyGroup(token, id);
			groups = groups.filter(group => group.id !== id);
			if (selectedGroupId === id) {
				selectedGroupId = 0;
				editedGroupName = '';
			}
		} catch (error) {
			console.error(error);
		}
	}
</script>

<Modal bind:show>
	<div class="p-5">
		<div class="flex justify-between items-center mb-4">
			<div class="text-lg font-medium">{$i18n.t('Groups')}</div>
			<button
				class="text-gray-500 hover:text-gray-700"
				on:click={() => {
					show = false;
				}}
			>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
				</svg>
			</button>
		</div>

		<div class="flex justify-end items-center mb-4">
			{#if addGroupInput}
				<input type="text" bind:value={newGroupName} placeholder="Name" class="w-5/6 rounded-lg py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 disabled:text-gray-500 dark:disabled:text-gray-500 outline-none" />
				<button class="w-1/6 ml-2.5 px-2 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg" type="button" on:click={createGroup}>Create</button>
			{:else}
				<Tooltip content="Add Group">
					<button
						class="px-2 py-2 rounded-xl border border-gray-200 dark:border-gray-600 dark:border-0 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition font-medium text-sm flex items-center space-x-1"
						on:click={() => {
									addGroupInput = !addGroupInput;
								}}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 16 16"
							fill="currentColor"
							class="w-4 h-4"
						>
							<path
								d="M8.75 3.75a.75.75 0 0 0-1.5 0v3.5h-3.5a.75.75 0 0 0 0 1.5h3.5v3.5a.75.75 0 0 0 1.5 0v-3.5h3.5a.75.75 0 0 0 0-1.5h-3.5v-3.5Z"
							/>
						</svg>
					</button>
				</Tooltip>
			{/if}
		</div>

		<div class="mb-4">
			<div class="relative overflow-x-auto">
				<table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
					<thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
					<tr>
						<th scope="col" class="px-6 py-3">Group Name</th>
						<th scope="col" class="px-6 py-3 text-right">Actions</th>
					</tr>
					</thead>
					<tbody>
					{#each groups as group}
						<tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
							{#if selectedGroupId !== 0 && selectedGroupId === group.id}
								<td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
									<input type="text" bind:value={editedGroupName} class="w-full rounded py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-850 disabled:text-gray-500 dark:disabled:text-gray-500 outline-none" />
								</td>
							{:else}
								<td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
									{group.name}
								</td>
							{/if}

							<td class="px-6 py-4 text-right">
								{#if selectedGroupId !== 0 && selectedGroupId === group.id}
									<button class="ml-2 px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg" on:click={editGroup}>Save</button>
								{:else}
									<div class="flex gap-0.5 justify-end">

										<Tooltip content={$i18n.t('Edit Group')}>
											<button
												class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
												on:click={() => { selectGroup(group.id) }}>
												<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
														 stroke="currentColor" class="w-4 h-4">
													<path stroke-linecap="round" stroke-linejoin="round"
																d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125" />
												</svg>
											</button>
										</Tooltip>

										<Tooltip content={$i18n.t('Delete Group')}>
											<button
												class="self-center w-fit text-sm px-2 py-2 hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
												on:click={() => { deleteGroup(group.id) }}>
												<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
														 stroke="currentColor" class="w-4 h-4">
													<path stroke-linecap="round" stroke-linejoin="round"
																d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
												</svg>
											</button>
										</Tooltip>
									</div>
								{/if}
							</td>
						</tr>
					{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
</Modal>
