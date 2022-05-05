import tkinter as tk
from InvestmentTracker import Controller
from tkinter.ttk import Combobox, Scrollbar
from SimpleCalendar import SimpleCalendar
from tkinter.simpledialog import askstring, askinteger, askfloat
from tkinter.messagebox import showwarning


class App:
    STARTING_CLIENTS = ("Ellen Turing", "Bill Fences",
                        "Steve Employments", "Elon Tusk")
    STARTING_STOCKS = (("AAPL", 165.63), ("TSLA", 975.93),
                       ("MSFT", 285.20), ("NVDA", 219.17), ("NCNO", 42.21))
    ACTIONS = ("Buy", "Sell")
    TITLE = "Investopia"
    SUBTITLE = "Investment Tracking Simulation"
    INSTRUCTIONS = "Select a client, select an action, type an amount, select a stock, and then click 'Process' to process a transaction. When you are all \nset click the 'EOD' button to go to the next day."
    FONT_FAMILY = "ARIAL"
    CLIENT_PROMPT = "Select a client:"
    ACTION_PROMPT = "Select an action:"
    STOCK_PROMPT = "Select a stock:"
    AMOUNT_BUY_PROMPT = "Enter a dollar amount to invest:"
    AMOUNT_SELL_PROMPT = "Enter a number of stocks to sell:"
    PROCESS_PROMPT = "PROCESS"
    AMOUNT_ERROR = "Please enter a positive number\n(exclude all symbols)"
    REQUIRED_ERROR = "Missing required field(s)"
    AGG_PRICE = "Weekly Aggregate\n Change in Investments"
    AGG_PERCENT = "Weekly Aggregate\nPercent Change"
    OBS_CLIENT = "Client Observers"
    OBS_STOCK = "Stock Observers"
    EOD_PROMPT = "EOD"

    def __init__(self):
        # CONTOROLLER
        self.controller: Controller = Controller()
        for client in App.STARTING_CLIENTS:
            self.controller.register_client(client)
        for ticker, price in App.STARTING_STOCKS:
            self.controller.register_stock(ticker, price)

        # ROOT
        self.root: tk.Tk = tk.Tk()
        self.root.title(App.TITLE)
        self.root.geometry('1150x400')

        # MENU
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=App)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Add Client", command=self.add_client)
        editmenu.add_command(label="Add Stock", command=self.add_stock)
        editmenu.add_separator()
        editmenu.add_command(label="Remove Client", command=self.remove_client)
        editmenu.add_command(label="Remove Stock", command=self.remove_stock)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.root.config(menu=menubar)

        # HEADER
        self.header: tk.Frame = tk.Frame(self.root, bd='5')
        self.header.grid(column=0, row=0, columnspan=3)
        tk.Label(self.header, text=App.TITLE, font=(
            App.FONT_FAMILY, 25, "bold")).pack()
        tk.Label(self.header, text=App.SUBTITLE, font=(
            App.FONT_FAMILY, 25, "italic")).pack()
        tk.Label(self.header, text=App.INSTRUCTIONS).pack()

        # LEFT - UI
        self.left: tk.Frame = tk.Frame(
            self.root,
            bd=5,
        )
        self.left.grid(column=0, row=1)

        tk.Label(self.left, text=App.CLIENT_PROMPT).pack()
        self.client_select = Combobox(
            self.left,
            height=5,
            postcommand=self.update_visible_clients,
            state='readonly',
            textvariable=tk.StringVar()
        )
        self.client_select.pack()

        self.action_frame = tk.Frame(
            self.left,
            bd=5
        )
        self.action_frame.pack()
        self.action_select = tk.StringVar()
        self.buy_radio = tk.Radiobutton(
            self.action_frame,
            text='Buy',
            variable=self.action_select,
            value='Buy',
            command=self.update_amount_prompt
        )
        self.buy_radio.select()
        self.buy_radio.pack(side="left")
        self.sell_radio = tk.Radiobutton(
            self.action_frame,
            text='Sell',
            variable=self.action_select,
            value='Sell',
            command=self.update_amount_prompt
        )
        self.sell_radio.pack(side="right")

        tk.Label(self.left, text=App.STOCK_PROMPT).pack()
        self.stock_select = Combobox(
            self.left,
            height=5,
            postcommand=self.update_visible_stocks,
            state='readonly',
            textvariable=tk.StringVar()
        )
        self.stock_select.pack()

        self.amount_label = tk.Label(
            self.left,
            text=App.AMOUNT_BUY_PROMPT
        )
        self.amount_label.pack()
        self.amount_entry = tk.Entry(
            self.left,
            width=9,
            textvariable=tk.StringVar()
        )
        self.amount_entry.pack()

        self.process_button = tk.Button(
            self.left,
            text=App.PROCESS_PROMPT,
            command=self.process
        )
        self.process_button.pack()
        self.process_response_label = tk.Label(self.left)
        self.process_response_label.pack()

        # CENTER - AGG STATS
        self.center = tk.Frame(
            self.root,
            bd=5
        )
        self.center.grid(column=1, row=1)

        self.today_label = tk.Label(
            self.center,
            font=(App.FONT_FAMILY, 20),
            text=SimpleCalendar.get_today()
        )
        self.today_label.pack()

        self.agg_change = tk.Frame(self.center, bd=5)
        self.agg_change.pack()
        tk.Label(self.agg_change, text=App.AGG_PRICE).grid(column=0, row=0)
        self.agg_price_change_data = tk.Label(
            self.agg_change,
            font=(App.FONT_FAMILY, 18),
            text=f'${round(self.controller.agg_price_change, 2)}'
        )
        self.agg_price_change_data.grid(column=0, row=1)
        tk.Label(self.agg_change, text=App.AGG_PERCENT).grid(column=1, row=0)
        self.agg_percent_change_data = tk.Label(
            self.agg_change,
            font=(App.FONT_FAMILY, 18),
            text=f'{round(self.controller.agg_percent_change,2)}%'
        )
        self.agg_percent_change_data.grid(column=1, row=1)

        eod_button = tk.Button(
            self.center,
            text=App.EOD_PROMPT,
            command=self.eod
        )
        eod_button.pack()

        # RIGHT - OBS STATS
        self.right = tk.Frame(self.root, bd=5)
        self.right.grid(column=2, row=1)

        # CLIENTS
        tk.Label(self.right, text=App.OBS_CLIENT).grid(column=0, row=0)

        self.clients_data = tk.Frame(self.right)
        self.clients_data.grid(column=0, row=1)

        self.update_client_stats()

        # STOCKS
        tk.Label(self.right, text=App.OBS_STOCK).grid(column=1, row=0)

        self.stocks_data = tk.Frame(self.right)
        self.stocks_data.grid(column=1, row=1)

        self.update_stock_stats()

        self.root.mainloop()

    def update_visible_clients(self):
        self.client_select['values'] = [
            str(c.id) + ' ' + c.name for c in self.controller.client_observers]

    def update_visible_stocks(self):
        self.stock_select['values'] = [
            s.ticker for s in self.controller.stock_observers]

    def update_amount_prompt(self):
        if self.action_select.get() == "Buy":
            self.amount_label['text'] = App.AMOUNT_BUY_PROMPT
        else:
            self.amount_label['text'] = App.AMOUNT_SELL_PROMPT
        self.amount_entry.delete(0, tk.END)

    def process(self):
        if not self.valid_amount():
            self.process_response_label['text'] = App.AMOUNT_ERROR
            self.process_response_label['fg'] = 'red'
        elif not self.client_select.get() or not self.amount_entry.get() or not self.stock_select.get():
            self.process_response_label['text'] = App.REQUIRED_ERROR
            self.process_response_label['fg'] = 'red'
        else:
            for client in self.controller.clients:
                if client.ID == int(self.client_select.get().split()[0]):
                    break
            for stock in self.controller.stocks:
                if stock.TICKER == self.stock_select.get():
                    break
            if self.action_select.get() == "Buy":
                client.invest(stock, float(self.amount_entry.get()))
                self.process_response_label['text'] = f'{client.name} successfully invested ${self.amount_entry.get()} into {stock.TICKER}'
                self.process_response_label['fg'] = 'green'
                self.update_client_stats()
            elif self.action_select.get() == "Sell":
                if client.sell(stock, float(self.amount_entry.get())):
                    self.process_response_label['text'] = f'{client.name} successfully sold {self.amount_entry.get()} share(s) of {stock.TICKER}'
                    self.process_response_label['fg'] = 'green'
                    self.update_client_stats()
                else:
                    self.process_response_label['text'] = f'{client.name} doesn\'t own {self.amount_entry.get()} share(s) of {stock.TICKER}'
                    self.process_response_label['fg'] = 'red'

    def valid_amount(self):
        try:
            return True if float(self.amount_entry.get()) > 0 else False
        except ValueError:
            return False

    def eod(self):
        self.controller.eod()
        self.today_label['text'] = SimpleCalendar.get_today()
        if SimpleCalendar.get_today() == SimpleCalendar.SUN:
            self.agg_price_change_data['text'] = f'${round(self.controller.agg_price_change,2)}'
            self.agg_percent_change_data['text'] = f'{round(self.controller.agg_percent_change*100,2)}%'
        self.update_stock_stats()

    def update_client_stats(self):
        self.clients_data.destroy()
        self.clients_data = tk.Frame(self.right)
        self.clients_data.grid(column=0, row=1)

        self.clients_canvas = tk.Canvas(self.clients_data)
        self.clients_canvas.pack(side=tk.LEFT, fill='both', expand='yes')

        self.clients_scroll_bar = Scrollbar(
            self.clients_data,
            orient='vertical',
            command=self.clients_canvas.yview
        )
        self.clients_scroll_bar.pack(side=tk.RIGHT, fill="y")
        self.clients_canvas.configure(
            yscrollcommand=self.clients_scroll_bar.set)
        self.clients_canvas.bind('<Configure>', lambda a: self.clients_canvas.configure(
            scrollregion=self.clients_canvas.bbox('all')))

        self.clients_frame = tk.Frame(self.clients_canvas)
        self.clients_canvas.create_window(
            (150, 0),
            window=self.clients_frame
        )
        for i, client_obs in enumerate(self.controller.client_observers):
            tk.Label(self.clients_frame, text=client_obs.id).grid(
                column=0, row=2*i+1, rowspan=2)
            tk.Label(self.clients_frame, text=client_obs.name).grid(
                column=1, row=2*i+1, rowspan=2)
            tk.Label(
                self.clients_frame, text=f'-${round(client_obs.invested,2)}').grid(column=2, row=2*i+1)
            tk.Label(
                self.clients_frame, text=f'+${round(client_obs.received,2)}').grid(column=2, row=2*i+2)

    def update_stock_stats(self):
        self.stocks_data.destroy()

        self.stocks_data = tk.Frame(self.right)
        self.stocks_data.grid(column=1, row=1)

        self.stocks_canvas = tk.Canvas(self.stocks_data)
        self.stocks_canvas.pack(side=tk.LEFT, fill='both', expand='yes')

        self.stocks_scroll_bar = Scrollbar(
            self.stocks_data,
            orient='vertical',
            command=self.stocks_canvas.yview
        )
        self.stocks_scroll_bar.pack(side=tk.RIGHT, fill="y")
        self.stocks_canvas.configure(yscrollcommand=self.stocks_scroll_bar.set)
        self.stocks_canvas.bind('<Configure>', lambda b: self.stocks_canvas.configure(
            scrollregion=self.stocks_canvas.bbox('all')))

        self.stocks_frame = tk.Frame(self.stocks_canvas)
        self.stocks_canvas.create_window(
            (150, 0),
            window=self.stocks_frame
        )

        for i, stock_obs in enumerate(self.controller.stock_observers):
            tk.Label(self.stocks_frame, text=stock_obs.ticker).grid(
                column=2, row=2*i+1, rowspan=2)
            tk.Label(
                self.stocks_frame, text=f'${round(stock_obs.price,2)}').grid(column=3, row=2*i+1)
            tk.Label(
                self.stocks_frame, text=f'{round(stock_obs.percent_change,2)}%').grid(column=3, row=2*i+2)

    def add_client(self):
        try:
            self.root.withdraw()
            name = askstring('Add Client', 'Enter new client\'s name:').strip()
            if name:
                self.controller.register_client(name)
                self.update_client_stats()
            else:
                showwarning("Invalid Name", "Please enter a name")
            self.root.deiconify()
        except:
            self.root.deiconify()

    def remove_client(self):
        try:
            self.root.withdraw()
            id_ = int(askinteger('Remove Client',
                                 'Enter the Id of a current client:'))
            if id_ in [client_obs.id for client_obs in self.controller.client_observers]:
                self.controller.unregister_client(id_)
                self.update_client_stats()
            else:
                showwarning("Invalid Id", "This client does not exists")
            self.root.deiconify()
        except:
            self.root.deiconify()

    def add_stock(self):
        try:
            self.root.withdraw()
            ticker = askstring(
                'Add Stock', 'Enter new stock\'s ticker:').strip().upper()
            if ticker in [stock_obs.ticker for stock_obs in self.controller.stock_observers]:
                showwarning("Invalid Ticker", "This ticker already exists")
            elif ticker:
                price = askfloat("Add Stock", "Enter stock's current price:")
                self.controller.register_stock(ticker, price)
                self.update_stock_stats()
            else:
                showwarning("Invalid ticker", "Please enter a ticker")
            self.root.deiconify()
        except:
            self.root.deiconify()

    def remove_stock(self):
        try:
            self.root.withdraw()
            ticker = askstring(
                'Remove Stock', 'Enter the ticker of a current stock:').strip().upper()
            if ticker in [stock_obs.ticker for stock_obs in self.controller.stock_observers]:
                self.controller.unregister_stock(ticker)
                self.update_stock_stats()
            else:
                showwarning("Invalid ticker",
                            "This stock doesn't currently exist")
            self.root.deiconify()
        except:
            self.root.deiconify()


def main():
    App()


if __name__ == '__main__':
    main()
