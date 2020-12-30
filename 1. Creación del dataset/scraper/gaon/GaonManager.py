import time

from gaon.GaonStructuredData import GaonStructuredData
from gaon.GaonWebPage import GaonWebPage
from utils import PageRequester


class GaonManager:

    def save_songs(self, output, until=2014):
        """
        Scrape and save songs
        """
        try:
            # Get html
            requester = PageRequester()
            url_prefix = "http://www.gaonchart.co.kr/main/section/chart/" \
                         "online.gaon?nationGbn=T&serviceGbn=ALL"
            html = requester.get(url_prefix + "&termGbn=month")
            g = GaonWebPage(html)
            # get all months
            year_months = g.get_all_monthly_links_text(until=until)
            if len(year_monts) == 0:
                print("No songs found, try changing the limit year.")
            year_months.reverse()
            data = GaonStructuredData()
            remaining_time = None
            # For every month...
            for i, y in enumerate(year_months):
                print(f"{i + 1}/{len(year_months)}")
                start = time.time()
                gaon_month_page = GaonWebPage(year_month=y)
                # Build link
                link_params_month = gaon_month_page.build_link_params()
                link_month = f"{url_prefix}&{link_params_month}"
                # Get html
                html_month = requester.get(link_month)
                gaon_month_page.set_html(html_month)
                # Get songs
                data_month = gaon_month_page.get_songs()
                # Join data
                data.concatenate(data_month)

                if not remaining_time:
                    # Calculate the remaining time
                    end = time.time()
                    remaining_time = (end - start) * (
                            len(year_months) - 1) / 60
                    print(f"Remaining time: {remaining_time} minutes")
            data.data.loc[data.data.external_factors > 1, 'external_factors'] \
                = 1
            data.save_as(output)
        except Exception as e:
            print(e)
