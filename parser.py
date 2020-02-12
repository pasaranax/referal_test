from urllib.parse import urlparse


class Parser:
    def __init__(self, log, sort=False):
        if sort:
            self.log = sorted(log, key=lambda x: x["date"])
        else:
            self.log = log
        self.customers = {}

    def records(self, partner=None, only_purchases=False):
        """
        Yield customers for every log record
        :param partner: optional, yield only for selected partner
        :param only_purchases: optional, set True if need only purchases
        :return: Customer object
        """
        for record in self.log:
            if record["client_id"] not in self.customers:
                customer = Customer(record)
                self.customers[record["client_id"]] = customer
            else:
                customer = self.customers[record["client_id"]]
                customer.update(record)

            if not partner or partner == customer.last_partner:
                if not only_purchases or customer.purchase:
                    yield customer


class Customer:
    def __init__(self, record):
        self.client_id = None
        self.purchases = []
        self.last_partner = None
        self.last_record = None
        self.purchase = None
        self.update(record)

    def update(self, record):
        self.client_id = record["client_id"]
        self.last_record = record
        if record["document.referer"]:
            referer = urlparse(record["document.referer"]).netloc
            if referer != "shop.com":
                self.last_partner = referer
        if record["document.location"] == "https://shop.com/checkout":
            self.purchases.append({
                "partner": self.last_partner,
                "date": record["date"]
            })
            self.purchase = self.purchases[-1]
        else:
            self.purchase = None

    def __repr__(self):
        return f"Customer(client_id={self.client_id}, partner={self.last_partner}, purchase={self.purchase is not None})"
