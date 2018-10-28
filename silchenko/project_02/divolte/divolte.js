<script src="https://de3-00-divolte.loveflorida88.online/divolte.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
    $(document).ready(function() {
      // price from basket
      $('.basket-btn-checkout').click(function() {
        var basket_price = $('.basket-coupon-block-total-price-current').first().text().match(/\d+/g).map(Number).join('');
        divolte.signal('checkoutEvent', { basket_price: basket_price });
      });
      // item details
      $('.product-item-container').click(function() {
        var item_id = jQuery(this).attr("id");
        var item_price = $('.product-item-price-current', this).first().text().match(/\d+/g).map(Number).join('');
        divolte.signal('itemEvent', { item_id: item_id, item_price: item_price});
      });
    });
</script>
