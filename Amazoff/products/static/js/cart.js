var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('ProductId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user === 'AnonymousUser'){
			Swal.fire({
				icon: 'error',
				title: 'Login.',
				text: 'Please login to add to cart.',
			  })
		}
		else{
			updateUserOrder(productId, action)
		}
		
	})
}

function updateUserOrder(productId, action){
	console.log('User logged in, sending data...')
	var url = '/update_item/'

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
			title: 'Added!',
			text: 'Cart has been updated successfully!',
			footer: '<a href="/cart">Go to cart</a>'
		  })
	});
}

