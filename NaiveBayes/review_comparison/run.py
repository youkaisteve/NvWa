from amazon_crawl import AmazonCrawl

amazoncrawl = AmazonCrawl(
    '解忧杂货铺',
    'https://www.amazon.cn/product-reviews/B00JZ96ZI8/ref=cm_cr_arp_d_paging_btm_%d?pageNumber=%d',
    907)

amazoncrawl.run()
