<script>
	let destinations = [];
  
	async function loadDestinations() {
	  const response = await fetch('/api/destinations');
	  destinations = await response.json();
	}
  </script>
  
  <button on:click="{loadDestinations}">Load Destinations</button>
  
  {#if destinations.length > 0}
	<ul>
	  {#each destinations as destination}
		<li>{destination.name}</li>
	  {/each}
	</ul>
  {:else}
	<p>No destinations to display. Click the button to load destinations.</p>
  {/if}
  