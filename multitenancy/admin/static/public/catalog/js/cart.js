
var removeBtns = document.getElementById('btn-remove-to-basket')

for(let i = 0; i < removeBtns.length; i++){
  removeBtns[i].addEventListener('click', function(){
    let variant_id = this.dataset.variantId
    let action = this.dataset.action
    longclawclient.basketList.post({
      prefix: "{% longclaw_api_url_prefix %}",
      data: {
        variant_id:variant_id,
        //action: action 
      }
    });
    console.log('variant_id:', variant_id, 'action:', action);

  })
}
