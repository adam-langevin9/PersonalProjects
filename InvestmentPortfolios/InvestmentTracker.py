from SimpleCalendar import SimpleCalendar
from Observe import AObserver, AObservable
from Visit import AVisitor, AVisitable
from DoublyLinkedList import DLL
from random import uniform


class _Stock(AObservable):
    def __init__(self, ticker: str, price: float):
        self.__TICKER: str = ticker
        self.__price: float = price
        self.__observers: DLL[AObserver] = DLL()

    @property
    def TICKER(self):
        return self.__TICKER

    @property
    def price(self):
        return self.__price

    @property
    def observers(self):
        return self.__observers

    def __notify(self):
        for observer in self.__observers:
            observer.update(self)

    def update_price(self):
        self.__price = round(
            self.price + uniform(-self.price/3, self.price/3), 2)
        self.__notify()


class _StockObserver(AObserver):
    def __init__(self):
        self.__ticker: str = ''
        self.__price: float = 0.0
        self.__percent: float = 0.0

    @property
    def ticker(self):
        return self.__ticker

    @property
    def price(self):
        return self.__price

    @property
    def percent_change(self):
        return self.__percent

    def update(self, stock: _Stock):
        self.__ticker = stock.TICKER
        self.__percent = 0.0 if not self.__price else (
            stock.price - self.__price) / self.__price
        self.__price = stock.price


class _StockReceipt:
    def __init__(self, stock: _Stock, initial_investment: float):
        self.__stock: _Stock = stock
        self.__invested: float = initial_investment
        self.__shares: float = initial_investment/stock.price
        self.__received: float = 0

    @property
    def stock(self):
        return self.__stock

    @property
    def invested(self):
        return self.__invested

    @property
    def shares(self):
        return self.__shares

    def invest(self, investment: float):
        self.__invested += investment
        self.__shares += investment/self.__stock.price

    def sell(self, shares: float):
        if self.shares >= shares:
            self.__shares -= shares
            received = shares * self.__stock.price
            self.__received += received
            return received
        return 0.0

    def sell_all(self):
        shares = self.shares
        return self.sell(shares)


class _Client(AObservable):
    next_id: int = 1

    def __init__(self, name: str):
        self.__ID: int = _Client.next_id
        _Client.next_id += 1
        self.__name: str = name
        self.__purchased_stocks: DLL[_StockReceipt] = DLL()
        self.__invested: float = 0.0
        self.__received: float = 0.0
        self.__observers: DLL[AObserver] = DLL()

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def purchased_stocks(self):
        return self.__purchased_stocks

    @property
    def invested(self):
        return self.__invested

    @property
    def received(self):
        return self.__received

    @property
    def observers(self):
        return self.__observers

    def invest(self, stock: _Stock, investment: float):
        for receipt in self.__purchased_stocks:
            if receipt.stock == stock:
                self.__invested += investment
                receipt.invest(investment)
                self.notify()
                return
        self.__invested += investment
        self.__purchased_stocks.append(_StockReceipt(stock, investment))
        self.notify()

    def sell(self, stock: _Stock, shares: float):
        for receipt in self.__purchased_stocks:
            if receipt.stock == stock:
                received = receipt.sell(shares)
                self.__received += received
                self.notify()
                return received

    def payout(self, stock: _Stock):
        for receipt in self.__purchased_stocks:
            if receipt.stock == stock:
                received = receipt.sell_all()
                self.__received += received
                self.notify()
                return received

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class _ClientObserver(AObserver):
    def __init__(self):
        self.__id: int = 0
        self.__name: str = ''
        self.__invested: float = 0.0
        self.__received: float = 0.0

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def invested(self):
        return self.__invested

    @property
    def received(self):
        return self.__received

    def update(self, client: _Client):
        self.__id = client.ID
        self.__name = client.name
        self.__invested = client.invested
        self.__received = client.received


class _ClientPool(DLL, AVisitable):
    def __init__(self):
        self._DLL__hd: DLL.Node | None = None
        self._DLL__tl: DLL.Node | None = None
        self._DLL__size: int = 0

    def bulk_payout(self, stock: _Stock):
        for client in self:
            client.payout(stock)


class _AggPriceChangeVisitor(AVisitor):
    def __init__(self):
        self.__agg_price = 0

    def visit(self, clients: _ClientPool):
        old_agg_price: float = self.__agg_price
        self.__agg_price = 0
        for client in clients:
            for receipt in client.purchased_stocks:
                self.__agg_price += receipt.shares * receipt.stock.price
        return self.__agg_price - old_agg_price


class _AggPercentChangeVisitor(AVisitor):
    def __init__(self):
        self.__agg_price = 0

    def visit(self, clients: _ClientPool):
        old_agg_price: float = self.__agg_price
        self.__agg_price = 0
        for client in clients:
            for receipt in client.purchased_stocks:
                self.__agg_price += receipt.shares * receipt.stock.price
        return (self.__agg_price - old_agg_price) / old_agg_price if old_agg_price != 0 else 0.0


class Controller():
    def __init__(self):
        self.__clients: _ClientPool[_Client] = _ClientPool()
        self.__stocks: DLL[_Stock] = DLL()
        self.__agg_price_change_visitor: _AggPriceChangeVisitor = _AggPriceChangeVisitor()
        self.__agg_percent_change_visitor: _AggPercentChangeVisitor = _AggPercentChangeVisitor()
        self.__agg_price_change: float = 0.0
        self.__agg_percent_change: float = 0.0
        self.__client_observers: DLL[_ClientObserver] = DLL()
        self.__stock_observers: DLL[_StockObserver] = DLL()

    @property
    def clients(self):
        return self.__clients

    @property
    def stocks(self):
        return self.__stocks

    @property
    def agg_price_change(self):
        return self.__agg_price_change

    @property
    def agg_percent_change(self):
        return self.__agg_percent_change

    @property
    def client_observers(self):
        return self.__client_observers

    @property
    def stock_observers(self):
        return self.__stock_observers

    def register_client(self, name: str):
        client = _Client(name)
        self.__clients.append(client)
        new_obs = _ClientObserver()
        client.register(new_obs)
        self.__client_observers.append(new_obs)
        client.notify()
        return client

    def unregister_client(self, id_: int):
        for client in self.__clients:
            if client.ID == id_:
                break
        for receipt in client.purchased_stocks:
            client.payout(receipt)
        for obs in client.observers:
            self.__client_observers.remove(obs)
        self.__clients.remove(client)

    def register_stock(self, ticker: str, price: float):
        stock = _Stock(ticker, price)
        self.__stocks.append(stock)
        new_obs = _StockObserver()
        stock.register(new_obs)
        self.__stock_observers.append(new_obs)
        stock.notify()
        return stock

    def unregister_stock(self, ticker: str):
        for stock in self.__stocks:
            if stock.TICKER == ticker:
                break
        self.__clients.bulk_payout(stock)
        for obs in stock.observers:
            self.__stock_observers.remove(obs)
        self.__stocks.remove(stock)

    def eod(self):
        if SimpleCalendar.get_today() == SimpleCalendar.SAT:
            self.__agg_price_change = self.__clients.accept(
                self.__agg_price_change_visitor)
            self.__agg_percent_change = self.__clients.accept(
                self.__agg_percent_change_visitor)
        SimpleCalendar.eod()
        for stock in self.__stocks:
            stock.update_price()
