var updateBtns = document.getElementsByClassName('wishlist')

for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('ProductId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user === 'AnonymousUser'){
			alert('Please log in to add to wishlist.')
		}else{
			if (action === 'add') {
				alert("Item added successfully.")
			}else{
				alert("Item removed.")
			}
			updateUserWishlist(productId, action)
		}
		
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
		location.reload()
	});
}

