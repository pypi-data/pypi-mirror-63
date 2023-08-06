import copy
import random
import uuid
from typing import Optional

import maya
from jamboree import JamboreeNew as Jamboree
from jamboree.handlers.default.data import DataHandler
from loguru import logger

from linkkt_e2e_handlers import PortfolioHandler, RequirementsHandler
from linkkt_e2e_handlers.data import PriceGenerator


class SimulationCreator(object):
    """ 
        # Simulation Creator
        ---
        Create a simulation that we'll be able to run through the faust pipeline.

        * Requirements
        * Stochastic Data
        * Portfolios
        * TimeHandler
    """
    def __init__(self, start_balance=10000, session_id:str=uuid.uuid4().hex, ecount=10, exchange="fake_exchange", **kwargs) -> None:
        self.session:str = session_id
        self.episode_count = ecount
        self.exchange = exchange
        self.start_balance = start_balance
        self.assets = ["USD_BTC", "USD_ATL", "USD_TRX", "USD_ETH", "USD_BCH", "USD_XRP", "USD_EOS", "USD_XTZ", "USD_LINK", "USD_ADA"]
        
        
        # Generated hexes
        self.episodes = [uuid.uuid4().hex for i in range(self.episode_count)]
        self.user_id = uuid.uuid4().hex # We're generating a fake user id for the time being
        # 
        self._current_episode:Optional[str] = None
        self.processor = Jamboree()
        
        # Kwargs
        self.min_price = kwargs.get("min_price", 200)
        self.max_price = kwargs.get("max_price", 5000)
        self.varied = kwargs.get("is_varied", True)
        self.length = kwargs.get("length", 5000)


        # Blanks
        self.generated = None

    
    @property
    def current_episode(self) -> str:
        if self._current_episode is None:
            return uuid.uuid4().hex
        return self._current_episode

    @current_episode.setter
    def current_episode(self, _episode:str):
        self._current_episode = _episode

    @property
    def pricing(self):
        data_handler = DataHandler()
        data_handler.processor = self.processor
        data_handler["category"] = self.category
        data_handler["subcategories"] = self.subcategories
        return data_handler
    
    @property
    def category(self):
        return "markets"
    
    @property
    def subcategories(self):
        return {
            "market": "stock",
            "country": "US",
            "sector": "faaaaake",
            "episode": self.current_episode
        }

    @property
    def required(self):
        sub = self.subcategories
        sub.pop("episode")
        base = {
            "category": self.category,
            "subcategories": sub
        }
        ret_items = []
        for asset in self.assets:
            base = copy.copy(base)
            base['name'] = asset
            ret_items.append(base)
        return ret_items
    
    @property
    def active(self):
        """ Get all of the active requirements"""
        return self.requirements.assets

    @property
    def sampled_portfolio(self):
        """ Return a sample portfolio for the user """
        assest_num = len(self.assets)
        num_sample = random.randint(2, assest_num)
        asset_sample = random.sample(self.assets, num_sample)
        return asset_sample

    @property
    def generator(self):
        """ Price generator """
        price_generator = PriceGenerator()
        price_generator.episodes = self.episodes
        price_generator.assets = self.assets
        price_generator.starting_min = self.min_price
        price_generator.starting_max= self.max_price
        price_generator.is_varied= self.varied
        price_generator.length= self.length
        return price_generator


    @property
    def portfolio(self):
        """ """
        portfolio = PortfolioHandler(start_balance=self.start_balance)
        portfolio.processor = self.processor
        portfolio['session'] = self.session
        portfolio['exchange'] = self.exchange
        portfolio['user_id'] = self.user_id
        portfolio['episode'] = self.current_episode
        portfolio['live'] = False
        portfolio.reset()
        return portfolio

    @property
    def current_generated(self) -> dict:
        """ Get all of the prices for current episode """
        if self.generated is None:
            self.generator.generate_all_episodes()
        current_prices = self.generated
        return current_prices.get(self.current_episode, {})
    
    @property
    def requirements(self):
        requirements = RequirementsHandler()
        requirements.processor = self.processor
        requirements['name'] = f"general-{self.session}"
        requirements.reset()
        return requirements

    def generate(self):
        logger.info("Starting generator")
        self.generated = self.generator.generate_all_episodes()
        logger.success("Successfully finished generation of assets")
        # 

    def save_generated(self):
        """ Saving generated data for use in real life """
        logger.info("Saving generated data")
        current_pricing = self.pricing
        current_generated = self.current_generated
        for asset in self.assets:
            current_pricing['name'] = asset
            data = current_generated.get(asset)
            current_pricing.reset()
            current_pricing.store_time_df(data, is_bar=True)
    
    def load_requirements(self):
        required_items = self.required
        self.requirements.asset_update(required_items)

    def load_assets(self):
        """ Loads the user's assets into the portfolio """
        user_sample = self.sampled_portfolio
        current_portfolio = self.portfolio
        for asset in user_sample:
            current_portfolio.add_asset(asset, self.subcategories)
    
    def load_allocation(self):
        current_portfolio = self.portfolio
        current_portfolio.is_inner_allocation = True
        current_portfolio.step_price()
        current_portfolio.is_inner_allocation = False
    
    def adjust_time(self):
        """
            portfolio_hand.time.head = maya.now().add(weeks=25)._epoch
            portfolio_hand.time.change_stepsize(microseconds=0, days=1, hours=0)
            portfolio_hand.time.change_lookback(microseconds=0, weeks=25, hours=0)
        """
        self.portfolio.time.head = maya.now().add(weeks=25)._epoch
        self.portfolio.time.change_stepsize(microseconds=0, days=1, hours=0)
        self.portfolio.time.change_lookback(microseconds=0, weeks=25, hours=0)

    
    def start_debug(self):
        self.load_requirements()

    def start(self):
        """ Create all of the episodes"""
        self.load_requirements()
        self.generate()
        logger.info("Successfully starting session")
        for episode in self.episodes:
            self.current_episode = episode
            self.save_generated()
            self.adjust_time()
            self.load_assets()
            self.load_allocation()

            
        


if __name__ == "__main__":
    simulation_creator = SimulationCreator(length=2000, ecount=1)
    simulation_creator.start_debug()

    # Get all of the active assets in the simulation
    active_assets = simulation_creator.active
    
    current_active = copy.copy(active_assets)
    random.shuffle(current_active)

    while True:
        current_asset = current_active.pop()
        simulation_creator.requirements.report(current_asset)
        # with simulation_creator.requirements.lock():
        if simulation_creator.requirements.is_valid:
            logger.debug(f"All assets finished. Starting next step {current_asset}")
            simulation_creator.requirements.reset_reports()
            
            current_active = copy.copy(active_assets)
            random.shuffle(current_active)

        else:
            logger.error(f"Asset: {current_asset}")