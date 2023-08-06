# -*- coding: utf-8 -*-
from time import sleep
from .api import ListoAPI, TooManyRequests


class Banks(ListoAPI):
    def __init__(self, token, base_url):
        super(Banks, self).__init__(token, base_url)

    def get_bank_accounts(self):
        return self.make_request(method="GET", path="/banks/bank_transaction/facets") \
               .json()['facets']['bank_account']

    def upload_bank_files(self, file_stream, bank=None, account_number=None, currency=None, rfc_id=None):
        return self.make_request(method="POST", path="/banks/upload_bank_files", files={'file': file_stream},
          data= {"bank": bank,"account_number": account_number,"currency": currency,"rfc_id": rfc_id})\
               .json()['status']
    
    def get_bank_transactions(self, **kwargs):
        return self.make_request(method="GET", path="/banks/bank_transaction", params=kwargs) \
               .json()['hits']

