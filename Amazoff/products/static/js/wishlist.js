var updateBtns = document.getElementsByClassName('wishlist')

for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('ProductId:', productId, 'Action:', action)
		console.log('USER:', user)
		var item = document.getElementById(productId);
		if (action === 'add'){
			item.classList.remove('bi-heart');
			item.classList.add('bi-heart-fill');
			var check = "button-" + String(productId)
			document.getElementById(check).dataset.action = 'remove';
			document.getElementById(check).dataset.content = "Click to remove from wishlist.";
		}
		else if (action === 'remove'){
			item.classList.remove('bi-heart-fill');
			item.classList.add('bi-heart');
			var check = "button-" + String(productId)
			document.getElementById(check).dataset.action = 'add';
			document.getElementById(check).dataset.content = "Click to add to wishlist.";
		}
	  	updateUserWishlist(productId, action)
	})
}

function updateUserWishlist(productId, action){
	console.log('User logged in, sending data...')
	var url = '/update_wishlist/'

	fetch(url, {
		method: 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productId': productId, 'action': action})
	})

	.then((response) => {
		return response.json()
	})

	.then((data) => {
		console.log('Data:', data)
		Swal.fire({
			icon: 'success',
			title: 'Updated',
			text: 'Your wishlist was updated',
		  })
	});
}

