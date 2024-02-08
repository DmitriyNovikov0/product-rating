import Kaspi_data as kd

PRODUCT = 'xiaomi'


kaspi = kd.Kaspi_data('https://kaspi.kz/shop/search/', product=PRODUCT, test=False, hideBrouser=True)
kaspi.get_date(start_page=50, end_page=140)
kaspi.saving_data()
