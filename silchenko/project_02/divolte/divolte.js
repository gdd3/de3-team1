<script src="https://de3-00-divolte.loveflorida88.online/divolte.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
    $(document).ready(function() {
      $('.basket-btn-checkout').click(function() {
        var price_text = $('.basket-coupon-block-total-price-current').first().text().match(/\d+/g).map(Number).join('');
        // console.log(price_text);
        divolte.signal('checkoutEvent', { price: price_text });
      });
    });
</script>
