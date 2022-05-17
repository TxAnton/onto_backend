import asyncio
import time

from neo4j import GraphDatabase

from ..Models.FastAPI_helper import FastAPI_M


class NeoDAO:
    def __init__(self, app: FastAPI_M):
        self.user = app.state.config.neo_user
        self.pwd = app.state.config.neo_pwd
        self.uri = app.state.config.neo_url
        self.timeout_sec = app.state.config.neo_timeout
        self.driver = self.get_driver()

    def get_driver(self):
        driver = None
        t = time.time()
        while not driver and time.time() - t <= self.timeout_sec:
            try:
                # with nostdout():
                driver = GraphDatabase.driver(self.uri, auth=(self.user, self.pwd))
            except:
                time.sleep(1)
        if not driver:
            raise Exception(f"Neo4j connection timed out after {self.timeout_sec} sec")
        return driver

    async def exec(self, statement, *args, **kwargs):
        """Run a statement asynchronously using the event loop's default thread
        pool executor.
        """
        driver = self.get_driver()

        def run():
            transaction = lambda tx: tx.run(statement).values()
            with self.driver.session() as session:
                return session.write_transaction(transaction)

        loop = asyncio.get_event_loop()
        # Passing None uses the default executor
        return await loop.run_in_executor(None, run)

    async def hello_world(self):
        message = "hello"
        q = "CREATE (a:Greeting) " \
            f"SET a.message = '{message}' " \
            "RETURN a.message + ', from node ' + id(a)"
        res = await self.exec(q)
        return res

    def __del__(self):
        self.driver.close()
