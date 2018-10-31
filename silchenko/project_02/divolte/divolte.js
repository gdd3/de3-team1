<script src="https://de3-00-divolte.loveflorida88.online/divolte.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script>
      $(document).ready(function() {
        $('.basket-btn-checkout').click(function() {
          var basket_price = $('.basket-coupon-block-total-price-current').first().text().match(/\d+/g).join('');
          divolte.signal('checkoutEvent', { basket_price: basket_price });
        });

      $('.product-item-image-wrapper').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $(this).attr("href");
        divolte.signal('itemViewEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.product-item-title a').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $(this).attr("href");
        divolte.signal('itemViewEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.product-item-button-container').click(function() {
        var item_container = $(this).closest('.product-item-container');
        var item_id = item_container.attr("id");
        var item_price = $('.product-item-price-current', item_container).first().text().match(/\d+/g).join('');
        var item_url = $('.product-item-image-wrapper', item_container).attr("href");
        divolte.signal('itemBuyEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

      $('.btn.btn-primary.product-item-detail-buy-button').click(function() {
        var item_id = $('.bx-catalog-element.bx-vendor').attr("id");
        var item_price = $('.product-item-detail-price-current').first().text().match(/\d+/g).join('');
        var item_url = $(location).attr("href");
        divolte.signal('itemBuyEvent', {
            item_id: item_id,
            item_price: item_price,
            item_url: item_url
          }
        );
      });

    });
</script>
