let $container = $('#cupcakes-container');
showCupcakes();

//this function creates HTML for cupcake data. It is called in showCupcakes(), searchCupcakes(), and newCupcake()
function makeCupcakeHTML(cupcake) {
	return `
        <div class="card m-2 col-md-4">
            <img src="${cupcake.image}" class="card-img-top" style="max-height: 15rem; object-fit: cover;"alt="A picture of a cupcake">
            <div class="card-body">
                <h5 class="card-title">${cupcake.flavor.toUpperCase()}</h5>
                <p class="card-text"><b>Rating:</b> ${cupcake.rating}</p>
                <p class="card-text"><b>Size:</b> ${cupcake.size}</p>
                <button data-id=${cupcake.id} class="btn btn-danger m-2 delete">Delete Cupcake</button>
				<a href="/cupcake/${cupcake.id}" class="btn btn-info m-2 view">View Cupcake</a>
            </div>
        </div>
`;
}

//this function creates an HTML message to be shown when a cupcake search returns no results
function badSearch(searchTerm) {
	return `<p class="bad-search">We're sorry, but we don't have any <b>${searchTerm}</b> cupcakes!</p>`;
}

// ################################################################################
// DISPLAY ALL CUPCAKES
// ################################################################################
async function showCupcakes() {
	let resp = await axios.get('/api/cupcakes');
	let cupcakes = resp.data.cupcakes;
	for (let cupcake of cupcakes) {
		$container.append(makeCupcakeHTML(cupcake));
	}
}

// ################################################################################
// SEARCH FOR CUPCAKES
// ################################################################################
async function searchCupcakes(searchTerm) {
	let resp = await axios.post('/api/cupcakes/find', (json = { searchTerm }));
	let cupcakes = resp.data.cupcakes;
	if (cupcakes.length > 0) {
		for (let cupcake of cupcakes) {
			$container.append(makeCupcakeHTML(cupcake));
		}
	} else {
		$container.append(badSearch(searchTerm));
	}
}

$('#search-form').on('submit', async function(evt) {
	evt.preventDefault();
	let searchTerm = $('#search').val();
	$container.empty();
	searchCupcakes(searchTerm);
});

// ################################################################################
// CREATE NEW CUPCAKE
// ################################################################################

$('#new-cupcake').on('submit', async function(evt) {
	evt.preventDefault();
	let flavor = $('#flavor').val();
	let size = $('#size').val();
	let rating = $('#rating').val();
	let image = $('#image').val();

	const newCupcake = await axios.post('/api/cupcakes', {
		flavor,
		size,
		rating,
		image
	});

	$container.append(makeCupcakeHTML(newCupcake.data.cupcake));

	$('#new-cupcake').each(function() {
		this.reset();
	});
});

// ################################################################################
// EDIT CUPCAKE
// ################################################################################

$('#edit-cupcake').on('submit', editCupcake);

async function editCupcake(evt) {
	evt.preventDefault();

	let cupcakeID = $('.edit-btn').data('id');
	let flavor = $('#flavor').val();
	let size = $('#size').val();
	let rating = $('#rating').val();
	let image = $('#image').val();

	let resp = await axios.post(`/api/cupcakes/${cupcakeID}`, {
		flavor,
		size,
		rating,
		image
	});

	let editedCupcake = resp.data.cupcake;

	$('.image').attr('src', editedCupcake.image);
	$('.flavor').text(editedCupcake.flavor.toUpperCase());
	$('.rating').text(editedCupcake.rating);
	$('.size').text(editedCupcake.size);
}

// ################################################################################
// DELETE CUPCAKE
// ################################################################################

async function deleteCupcake() {
	let cupcakeID = $(this).data('id');
	await axios.delete(`/api/cupcakes/${cupcakeID}`);
	$(this).parent().parent().remove();
}

$container.on('click', '.delete', deleteCupcake);
