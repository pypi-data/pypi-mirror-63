# -*-coding:utf-8 -*-

# @Time    : 2020/2/8 14:29
# @File    : strategy.py
# @User    : yangchuan
# @Desc    : quant trade strategy information
from quant_trade_framework.stock.context import Context
from quant_trade_framework.common.constant import Constant
from datetime import timedelta
from quant_trade_framework.common.logConfig import Logger
from quant_trade_framework.model.indicators import *
import math
from pytz import timezone
from quant_trade_framework.stock.account import Account
import pandas as pd
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line,Bar,Page
from pyecharts.components import Table
from quant_trade_framework.common.redisConfig import RuntimeConfig
from quant_trade_framework.common.admin import UserManager

logger = Logger.module_logger("system")
cst_tz = timezone('Asia/Shanghai')
utc_tz = timezone('UTC')


class Strategy:
    """
    class strategy define:
    (1) account: exchange,type,position
    (2) universe
    (3) strategy
    (4) strategy run
    """

    def __init__(self):
        """"""
        self.context = Context()
        self.daily_value = []
        self.profit_and_loss = []
        self.daily_return = []
        self.benchmark_daily_return = []
        self.run_datetimes = []
        self.strategy_annualized_returns = None
        self.annualised_benchmark_return = None
        self.cumulative_portfolio_return = None
        self.cumulative_benchmark_return = None
        self.algorithm_volatility = 0
        self.benchmark_volatility = 0
        self.alpha = 0
        self.sharpe_ratio = 0
        self.information_ratio = 0
        self.beta = 0
        self.annualized_portfolio_volatility = 0
        self.max_drawdown = 0
        self.start_daily_value = None
        self.total_return = None
        self.run_duration_in_days = 1
        self.start_benchmark_index = 0
        self.last_benchmark_index = 0
        self.start_protfolio_value = 0
        self.sortino_ratio = 0
        self.risk_free_ratio = 0.01
        self.average_change = 0
        self.downside_risk = 0
        self.RF = 0.04
        self.flag_cache_bar = False
        self.flag_prefetch_data = False

    def create_account(self,name:str,balance:float,
                       account_type:str):
        """
        create account
        :param name:str, account name
        :param exchange:str, exchange name,not used
        :param account_type:str, account type name,not used
        :param position_base: position dict,account's positions
        :return:
        """
        new_account = Account(name, balance, account_type)
        self.context.set_account(new_account)
        new_account.set_context(self.context)

    def create_universe(self,universe:str):
        """
        not used
        :param universe:
        :return:
        """
        self.universe = universe
        self.context.symbol = universe
        return universe

    def create_strategy(self,
                        initialize:object,
                        handle_data:object,
                        frequency:str,
                        flag_cache_bar:bool=False,
                        flag_prefetch_data:bool=False):
        """
        @param initialize: initialize function handler
        @param handle_data: every cycle function handler
        @param frequency: run frequency
        @param flag_cache_bar:
        @param flag_prefetch_data:
        @return:
        """
        self.initialize = initialize
        self.handle_data = handle_data
        self.frequency = frequency
        self.flag_cache_bar = flag_cache_bar
        self.flag_prefetch_data = flag_prefetch_data

        if self.frequency == Constant.RUN_FREQ_DAY:
            Context.run_freq = Constant.KLINE_INTERVAL_1DAY
        elif self.frequency == Constant.RUN_FREQ_HOUR:
            Context.run_freq = Constant.KLINE_INTERVAL_1HOUR
        elif self.frequency == Constant.RUN_FREQ_MINUTE:
            Context.run_freq = Constant.KLINE_INTERVAL_1MINUTE

    def backtest(self,start:str,end:str,run_at_time:str):
        """
        backtest configuration
        :param start: strategy fun start datetime
        :param end: strategy fun end datetime
        :param commission: commission parameters
        :param run_at_time: every cycle run time point
        :return: None
        """
        if run_at_time and run_at_time!= "":
            self.start = datetime.strptime(start + " " + run_at_time,"%Y-%m-%d %H:%M:%S")
            self.end = datetime.strptime(end + " " + run_at_time,"%Y-%m-%d %H:%M:%S")
        else:
            self.start = datetime.strptime(start, "%Y-%m-%d")
            self.end = datetime.strptime(end, "%Y-%m-%d")
        diff = self.end - self.start
        self.run_times = diff.days + 1
        self.run_duration_in_days = diff.days
        self.run_at_time = run_at_time
        self.context.set_current_datetime(self.start)
        self.run_backtest()



    def run_backtest(self):
        """
        run backtest logical in every cycle
        :return: None
        """
        self.initialize(self.context)
        user_verify = UserManager.user_verify(self.context.user_name,
                                              self.context.user_pwd)
        backtest_pre_start_flag = 0
        if user_verify:
            self.context.set_current_datetime(self.start)
            # self.before_start_operation()
            if self.flag_prefetch_data:
                temp_datetime = self.start - timedelta(days=1)
                self.context.prefetch_data(self.universe,None,temp_datetime,count=self.context.bars_size)
            runtime_config_obj = RuntimeConfig()
            if self.frequency == Constant.RUN_FREQ_DAY:
                for item in range(0,self.run_times):
                    temp = self.start + timedelta(days=item)
                    datetime_now_date_str = temp.strftime('%Y-%m-%d')
                    if runtime_config_obj.check_day_is_valid_trade_day(datetime_now_date_str):
                        self.context.set_current_datetime(temp)
                        if backtest_pre_start_flag == 0:
                            self.before_start_operation()
                            backtest_pre_start_flag = 1
                        new_bar = self.context.get_price("000001.XSHE",self.context.run_freq)
                        self.context.bars.update_bar(new_bar)
                        # self.handle_data(self.context)
                        if self.flag_cache_bar:
                            if self.context.bars.inited:
                                self.handle_data(self.context)
                        else:
                            self.handle_data(self.context)
                        self.indicator_cal()
                    else:
                        logger.info("today is not trade day")
            self.after_end_operation()
            self.draw_plt()
        else:
            logger.error("user auth fail")

    def indicator_cal(self):
        """
        every cycle indicator caculate
        :return:  None
        """
        logger.info(self.context.current_datetime())
        self.run_datetimes.append(self.context.current_datetime())

        #caculate daily value
        temp_value = 0
        for name,account in self.context.accounts.items():
            temp_value  = temp_value + account.balance
            for name1,position in account.position.items():
                temp_price = self.context.get_price(name1,self.context.run_freq).close_price
                temp_value = temp_value + abs(position.available) * temp_price

        current_daily_value= round(temp_value, 5)
        logger.info("daily value:" + str(current_daily_value))
        self.daily_value.append(current_daily_value)

        # caculate daily return
        if len(self.daily_value) >= 2:
            last_daily_value = self.daily_value[-2]
            if last_daily_value ==0:
                current_daily_return = 0
                temp_profit_and_loss = 0
            else:
                temp = (current_daily_value/
                                     last_daily_value) - 1
                temp = round(temp, 5)
                current_daily_return = temp
                temp_profit_and_loss = round(current_daily_value - last_daily_value,2)
            self.profit_and_loss.append(temp_profit_and_loss)
            logger.info("daily return:" + str(current_daily_return))
            logger.info("profit or loss:" + str(temp_profit_and_loss))
            self.daily_return.append(current_daily_return)

        #caculate benchmark daily return
        if len(self.daily_value) >= 2:
            if self.last_benchmark_index == 0:
                temp_current_benchmark_index = 0
                current_benchmark_return = 0
            else:
                temp_current_benchmark_index = self.context.get_benchmark_price().close_price
                temp = (temp_current_benchmark_index/
                                                 self.last_benchmark_index) -1
                current_benchmark_return = round(temp, 5)
            logger.info("daily benchmark return:" + str(current_benchmark_return))
            self.benchmark_daily_return.append(current_benchmark_return)
            self.last_benchmark_index = temp_current_benchmark_index

        #display daily position
        for name,account in self.context.accounts.items():
            temp_str = ""
            for name1,position in account.position.items():
                temp_str = temp_str + "symbol:" +str(name1) + " position:" + str(position.available)
                temp_price = self.context.get_price(name1,self.context.run_freq).close_price
                temp_value = temp_value + abs(position.available) * temp_price
            logger.info("account:" + str(name) + " " + temp_str)


    def before_start_operation(self):
        """
        caculates methods before the strategy running
        :return: None
        """
        temp_value = 0
        for name, account in self.context.accounts.items():
            temp_value = temp_value + account.balance
        self.start_daily_value = round(temp_value, 5)
        logger.info("start daily value:" + str(self.start_daily_value))
        self.daily_value.append(self.start_daily_value)

        #get benchmark index
        self.start_benchmark_index = self.context.get_benchmark_price().close_price
        self.last_benchmark_index = self.start_benchmark_index
        logger.info("start benchmark index:" + str(self.start_daily_value))

        #get the start prorfolio value equal to start daily value in usdt
        self.start_protfolio_value = self.start_daily_value
        logger.info("start prorfolio value:" + str(self.start_protfolio_value))

    def after_end_operation(self):
        """
        caculates methods after the strategy running
        :return: None
        """
        #caculate total return
        if len(self.daily_value) >= 2 and self.start_daily_value:
            last_daily_value = self.daily_value[-1]
            temp = (last_daily_value /
                    self.start_daily_value) - 1
            temp = round(temp, 5)
            self.total_return = temp
        else:
            self.total_return = 0
        logger.info("total return:" + str(self.total_return))

        #caculate Total Annualized Returns
        if len(self.daily_value) >= 2 and self.start_daily_value:
            temp = pow((1 + self.total_return),365.0/self.run_duration_in_days) - 1
            temp = round(temp, 5)
            self.strategy_annualized_returns = temp
        else:
            self.strategy_annualized_returns = 0
        logger.info("Annualised Strategy Return:" + str(self.strategy_annualized_returns))

        #caculate Benchmark Annualized Returns
        if len(self.daily_value) >= 2 and self.start_daily_value and self.start_benchmark_index!=0:
            last_benchmart_value = self.context.get_benchmark_price().close_price
            benchmark_return = (last_benchmart_value /
                    self.start_benchmark_index) - 1

            temp = pow((1 + benchmark_return),365.0/self.run_duration_in_days) - 1
            temp = round(temp, 5)
            self.annualised_benchmark_return = temp
        else:
            self.annualised_benchmark_return = 0
        logger.info("benchmark annualized return:" + str(self.annualised_benchmark_return))

        #caculate Algorithm Volatility
        df = pd.DataFrame({'date':self.run_datetimes,'rtn':self.daily_return})
        self.algorithm_volatility = df['rtn'].std() * math.sqrt(365)
        logger.info("Algorithm Volatility:" + str(self.algorithm_volatility))

        #caculate Benchmark Volatility
        df = pd.DataFrame({'date': self.run_datetimes, 'rtn': self.benchmark_daily_return})
        self.benchmark_volatility = df['rtn'].std() * math.sqrt(365)
        logger.info("Benchmark Volatility:" + str(self.benchmark_volatility))

        # caculate information ratio
        df = pd.DataFrame({'date': self.run_datetimes, 'rtn': self.daily_return,
                           'benchmark_rtn':self.benchmark_daily_return})
        df['diff'] = df['rtn'] - df['benchmark_rtn']
        aunual_mean = df['diff'].mean() * 365
        aunual_std = df['diff'].std() * math.sqrt(365)
        self.information_ratio = aunual_mean / aunual_std
        logger.info("Information Ratio:" + str(self.information_ratio))

        #caculate sharp ratio
        if self.algorithm_volatility != 0:
            self.sharpe_ratio = (self.strategy_annualized_returns -
                                 self.RF) / self.algorithm_volatility
        else:
            self.sharpe_ratio = 0
        logger.info("Sharp Ratio:" + str(self.sharpe_ratio))

        #caculate beta
        df = pd.DataFrame({'date': self.run_datetimes, 'rtn': self.daily_return,
                           'benchmark_rtn': self.benchmark_daily_return})
        self.beta = df['rtn'].cov(df['benchmark_rtn']) / df['benchmark_rtn'].var()
        logger.info("Beta:" + str(self.beta))

        #caculate alpha
        self.alpha = self.strategy_annualized_returns - (self.RF + self.beta * (self.annualised_benchmark_return- self.RF))
        logger.info("Alpha:" + str(self.alpha))

        #caculate max drawdown
        df = pd.DataFrame({'date': self.run_datetimes, 'capital': self.daily_value[1:]})
        df.sort_values(by='date',inplace=True)
        df.reset_index(drop=True,inplace=True)

        df['max2here'] = df['capital'].cummax()
        df['dd2here'] = df['capital'] / df['max2here'] -1
        temp = df.sort_values(by='dd2here').iloc[0][['date','dd2here']]
        self.max_drawdown = temp['dd2here']
        end_date = temp['date']
        df = df[df['date'] <= end_date]
        start_date = df.sort_values(by='capital',ascending=False).iloc[0]['date']

        logger.info("Max Draw Down: " +str(self.max_drawdown)
                    + " start datetime:" + str(start_date)
                    + " end datetime:" + str(end_date))

        #caculate average change
        df = pd.DataFrame({'date': self.run_datetimes, 'rtn': self.daily_return})
        self.average_change = df['rtn'].mean()
        logger.info("average change:" + str(self.average_change))

        #caculate downside risk
        temp_strategy_return_length = len(self.daily_return)
        temp_value = 0
        for item_index in range(1,temp_strategy_return_length):
            temp_ave = np.mean(self.daily_return[0:item_index])
            if self.daily_return[item_index] <temp_ave:
                temp_value = temp_value + pow((self.daily_return[item_index] - temp_ave),2)
        self.downside_risk = math.sqrt(temp_value * 365 / temp_strategy_return_length)
        logger.info("downside risk:" + str(self.downside_risk))

        #caculate Sortino Ratio
        if self.downside_risk != 0:
            self.sortino_ratio = (self.strategy_annualized_returns - self.RF) / self.downside_risk
        else:
            self.sortino_ratio = 0
        logger.info("sortino ratio:" + str(self.sortino_ratio))

        #print order detail
        for name,account in self.context.accounts.items():
            for order in account.orders:
                logger.info(order.to_dict())

    def draw_plt(self):
        """
        draw some pictures and tables in html
        :return: html file in current user folder
        """
        page = Page(
            layout=Page.SimplePageLayout,
            page_title = "计算指标")

        table = Table()

        headers = ["指标名", "值"]
        rows = [
            ["总收益",self.total_return],
            ["策略年化收益", self.strategy_annualized_returns],
            ["基准年化收益", self.annualised_benchmark_return],
            ["策略波动率", self.algorithm_volatility],
            ["基准波动率", self.benchmark_volatility],
            ["信息比率", self.information_ratio],
            ["夏普比率", self.sharpe_ratio],
            ["beta", self.beta],
            ["alpha", self.alpha],
            ["最大回撤", self.max_drawdown],
            ["平均收益率", self.average_change],
            ["下行波动率", self.downside_risk],
            ["索提诺比率", self.sortino_ratio]
        ]
        table.add(headers, rows).set_global_opts(
            title_opts=opts.ComponentTitleOpts(title="指标")
        )
        line = Line(
            init_opts=opts.InitOpts(
                width="1024px"
            )
        )
        line.add_xaxis(self.run_datetimes)
        line.add_yaxis("每日收益率",self.daily_return)
        line.add_yaxis("基准每日收益率", self.benchmark_daily_return)
        line.set_global_opts(
            title_opts=opts.TitleOpts(title="收益率"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")])

        bar = Bar(
            init_opts=opts.InitOpts(
                width="1024px"
            )
        )
        bar.add_xaxis(self.run_datetimes)
        bar.add_yaxis("每日盈亏", self.profit_and_loss)
        bar.set_global_opts(
            title_opts=opts.TitleOpts(title="每日盈亏"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")])

        page.add(line,bar,table)

        page.render()

