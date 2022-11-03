
var updateBtns = document.getElementsByClassName('update-cart')

for(var t = 0; t < updateBtns.length; t++){
  updateBtns[t].addEventListener('click', function(){
    var variant_id = this.dataset.variantId
    var action = this.dataset.action
    
    longclawclient.basketList.post({
      prefix: "{% longclaw_api_url_prefix %}",
      data: {
        variant_id: variant_id,
        csrfmiddlewaretoken: "{{csrf_token}}",
      }
    });
    console.log('variant_id:', variant_id, 'action:', action);
    

    console.log('USER:', user)
    if(user === 'AnonymousUser'){
      console.log('Not logged in')
    }else{
      updateUserOrder(variant_id, action)
    }
  } )
}

function updateUserOrder(variant_id, action){
  console.log('User is Logged in, sending data...')
  
  var url = 'basket'
}